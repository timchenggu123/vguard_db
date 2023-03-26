package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"time"
)

var seededRand = rand.New(rand.NewSource(time.Now().UnixNano()))

func mockRandomBytes(length int, charset string) []byte {
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[seededRand.Intn(len(charset))]
	}
	return b
}

func createGPSStruct(line []string) GPSData {
	return GPSData{
		Timestamp:            line[0],
		Latitude:             line[1],
		Longitude:            line[2],
		Elevation:            line[3],
		Accuracy:             line[4],
		Bearing:              line[5],
		SpeedMetersPerSecond: line[6],
		Satellites:           line[7],
		Provider:             line[8],
		HDOP:                 line[9],
		VDOP:                 line[10],
		PDOP:                 line[11],
		GeoidHeight:          line[12],
		AgeOfDgpsData:        line[13],
		DgpsID:               line[14],
		Activity:             line[15],
		Battery:              line[16],
		Annotation:           line[17],
		DistanceMeters:       line[18],
		ElapsedTimeSeconds:   line[19],
	}
}

func dataTxGenerator(leng int) {
	// Open the CSV file
	file, err := os.Open("./datasets/dataset_gps.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	// Create a CSV reader
	r := csv.NewReader(file)
	r.Comment = '#'
	r.FieldsPerRecord = -1 // allow variable number of fields per record
	// Read all the lines into a slice of string slices
	lines, err := r.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	// Generate a random line number
	rand.Seed(time.Now().UnixNano())
	lineNum := rand.Intn(len(lines))

	// Print the random line
	log.Println(lines[lineNum])

	gpsData := createGPSStruct(lines[lineNum])

	fmt.Println(gpsData)

	//charset := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	for i := 0; i < NumOfValidators; i++ {
		q := make(chan *Proposal, MaxQueue)

		for i := int64(0); i < MsgLoad; i++ {
			q <- &Proposal{
				Timestamp:   time.Now().UnixMicro(),
				Transaction: gpsData,
			}
		}
		requestQueue = append(requestQueue, q)
	}
}

// txGenerator enqueues mock data entries to all message queues
/*func txGenerator(len int) {
	charset := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	for i := 0; i < NumOfValidators; i++ {
		q := make(chan *Proposal, MaxQueue)

		for i := int64(0); i < MsgLoad; i++ {
			q <- &Proposal{
				Timestamp:   time.Now().UnixMicro(),
				Transaction: mockRandomBytes(len, charset),
			}
		}
		requestQueue = append(requestQueue, q)
	}

	log.Infof("%d request queue(s) loaded with %d requests of size %d bytes", NumOfValidators, MsgLoad, MsgSize)
}*/

func serialization(m interface{}) ([]byte, error) {
	return json.Marshal(m)
}

func deserialization(b []byte, m interface{}) error {
	return json.Unmarshal(b, m)
}
