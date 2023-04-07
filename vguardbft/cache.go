package main

/*
The implementation of V-Guard follows a "cache more, lock less" policy. This design
reduces lock overhead and contention while storing more intermediate results.
Intermediate consensus information for data batches are stored separately in the
ordering and consensus phases.
*/

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"
	"sync"
)

// ordSnapshot stores consensus information for each block in the ordering phase
// the map stores <blockID, blockSnapshot>
var ordSnapshot = struct {
	m map[int64]*blockSnapshot
	sync.RWMutex
}{m: make(map[int64]*blockSnapshot)}

// cmtSnapshot stores consensus information for each block in the consensus phase
// the map stores <blockID, blockSnapshot>
var cmtSnapshot = struct {
	m map[int64]*blockSnapshot
	sync.RWMutex
}{m: make(map[int64]*blockSnapshot)}

type blockSnapshot struct {
	sync.RWMutex
	// The hash of the block
	hash []byte
	// The data entries
	entries map[int]Entry
	// The signatures collected from validators to be converted to a threshold signature
	sigs [][]byte
	// rcvSig is the threshold signature of this block
	tSig []byte
	// The booth of this block
	booth Booth
}

var vgTxMeta = struct {
	sync.RWMutex
	sigs     map[int][][]byte // <rangeId, sigs[]>
	hash     map[int][]byte
	blockIDs map[int][]int64 // <rangeId, []blockIDs>
}{
	sigs:     make(map[int][][]byte),
	hash:     make(map[int][]byte),
	blockIDs: make(map[int][]int64),
}

var vgTxData = struct {
	sync.RWMutex
	tx  map[int]map[string][][]Entry // map<consInstID, map<orderingBooth, []entry>>
	boo map[int]Booth                //<consInstID, Booth>
}{
	tx:  make(map[int]map[string][][]Entry),
	boo: make(map[int]Booth),
}

func insertDataToDB(cmtBoothID int, gps GPSData) {
	//res, err := sqliteDatabase.Exec("INSERT INTO gps_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
	dbName := "database_" + strconv.Itoa(int(ServerId(ServerID)))
	mysqlDatabase, err := sql.Open("mysql", "root:123@tcp(127.0.0.1:3306)/"+dbName)
	// Prepare the INSERT statement
	_, err = mysqlDatabase.Exec("INSERT INTO gps_data  VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
		cmtBoothID,
		gps.Timestamp,
		gps.Latitude,
		gps.Longitude,
		gps.Elevation,
		gps.Accuracy,
		gps.Bearing,
		gps.SpeedMetersPerSecond,
		gps.Satellites,
		gps.Provider,
		gps.HDOP,
		gps.VDOP,
		gps.PDOP,
		gps.GeoidHeight,
		gps.AgeOfDgpsData,
		gps.DgpsID,
		gps.Activity,
		gps.Battery,
		gps.Annotation,
		gps.DistanceMeters,
		gps.ElapsedTimeSeconds)
	if err != nil {
		log.Fatal(err)
	}
	mysqlDatabase.Close()
	//time.Sleep(1 * time.Second)
}

func storeVgTx(consInstID int) {
	vgTxData.RLock()
	ordBoo := vgTxData.tx[consInstID]
	cmtBoo := vgTxData.boo[consInstID]
	vgTxData.RUnlock()

	log.Infof("VGTX %d in Cmt Booth: %v | total # of tx: %d", consInstID, cmtBoo.Indices, vgrec.GetLastIdx()*BatchSize)

	for key, chunk := range ordBoo { //map<boo, [][]entries>
		log.Infof("ordering booth: %v | len(ordBoo[%v]): %v", key, key, len(chunk))
		for _, entries := range chunk {
			for _, e := range entries {
				//log.Infof("ts: %v; tx: %v", e.TimeStamp, hex.EncodeToString(e.Tx))
				log.Infof("ts: %v; tx: %v", e.TimeStamp, e.Tx)

				if 0 == ServerId(ServerID) {
					//print("Proposer!!")
					insertDataToDB(cmtBoo.ID, e.Tx)
					// Create the JSON payload
					participants := []int{}
					participants = cmtBoo.Indices[:len(cmtBoo.Indices)-1]
					payload := map[string]interface{}{
						//"participants": []int{4, 5, 6},
						"participants": participants,
					}

					// Marshal payload to JSON
					jsonPayload, err := json.Marshal(payload)
					if err != nil {
						panic(err)
					}

					//res, err := http.Get("http://127.0.0.1:9860/")
					//print(res)

					// Send the HTTP request
					url := "http://127.0.0.1:9860/end_of_booth"
					req, err := http.NewRequest("GET", url, bytes.NewBuffer(jsonPayload))
					if err != nil {
						log.Fatal(err)
					}
					req.Header.Set("Content-type", "application/json")
					resp, err := http.DefaultClient.Do(req)
					if err != nil {
						log.Fatal(err)
					}

					defer resp.Body.Close()
				}
				//else {
				//	print("Validator!!")
				//}

				// Check response status code
				//if resp.StatusCode != http.StatusOK {
				//	log.Fatalf("Unexpected status code: %d", resp.StatusCode)
				//}

			}
		}
	}
}
