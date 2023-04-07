package main

import (
	"database/sql"
	"encoding/gob"
	"errors"
	"io/ioutil"
	"net"
	"os"
	"strconv"
	"sync"

	_ "github.com/go-sql-driver/mysql"
	_ "github.com/mattn/go-sqlite3"
)

var requestQueue []chan *Proposal

// var sqliteDatabase *sql.DB
var mysqlDatabase *sql.DB

var concierge = struct {
	n [NOP][]*ConnDock // Three phases
	//b  map[int][]int //map[booth#] int{server blockIDs in this booth}
	mu sync.RWMutex
}{}

//var requestQueue = make(chan *Proposal, MaxQueue)

func initConns(numOfServers int) {
	// initialize concierge
	for i := 0; i < len(concierge.n); i++ {
		concierge.n[i] = make([]*ConnDock, numOfServers)
	}

	// initialize dialog conns
	for i := 0; i < len(dialogMgr.conns); i++ {
		dialogMgr.conns[i] = make(map[ServerId]ConnDock)
	}
}

var dialogMgr = struct {
	sync.RWMutex
	conns []map[ServerId]ConnDock
}{conns: make([]map[ServerId]ConnDock, NOP)}

type ConnDock struct {
	SID  ServerId
	conn *net.TCPConn
	enc  *gob.Encoder
	dec  *gob.Decoder
}

func connRegistration(sconn net.TCPConn, phase int) (ServerId, error) {

	concierge.mu.Lock()

	defer concierge.mu.Unlock()
	defer serverIdLookup.RUnlock()

	serverIdLookup.RLock()

	if sid, ok := serverIdLookup.m[sconn.RemoteAddr().String()]; ok {
		concierge.n[phase][sid] = &ConnDock{
			SID:  sid,
			conn: &sconn,
			enc:  gob.NewEncoder(&sconn),
			dec:  gob.NewDecoder(&sconn),
		}

		log.Infof("%s | new server registered | Id: %v -> Addr: %v\n", cmdPhase[phase], sid, sconn.RemoteAddr())
		return sid, nil
	} else {
		return -1, errors.New("incoming connection not recognized")
	}
}

func dialSendBack(m interface{}, encoder *gob.Encoder, phaseNumber int) {
	if encoder == nil {
		log.Errorf("%s | encoder is nil", rpyPhase[phaseNumber])
	}
	if err := encoder.Encode(m); err != nil {
		log.Errorf("%s | send back failed | err: %v", rpyPhase[phaseNumber], err)
	}
}

func createDB(id string) {
	log.Println("Creating sqlite-database.db...")
	file, err := os.Create("./database/vehicledb_" + id + ".db") // Create SQLite file
	if err != nil {
		log.Fatal(err.Error())
	}
	file.Close()
	log.Println("sqlite-database.db created")
}

func takingInitRoles(proposer ServerId) {
	createDB(strconv.Itoa(int(ServerId(ServerID))))
	var err error
	//sqliteDatabase, err = sql.Open("sqlite3", "../database_"+strconv.Itoa(int(ServerId(ServerID)))+".db") // Open the created SQLite File
	dbName := "database_" + strconv.Itoa(int(ServerId(ServerID)))
	mysqlDatabase, err := sql.Open("mysql", "root:123@tcp(127.0.0.1:3306)/")
	if err != nil {
		panic(err)
	}
	defer mysqlDatabase.Close()

	// Create a new database for the current node if it does not exist
	_, err = mysqlDatabase.Exec("CREATE DATABASE IF NOT EXISTS " + dbName)
	if err != nil {
		panic(err.Error())
	}

	// switch to the database
	_, err = mysqlDatabase.Exec("USE " + dbName)
	if err != nil {
		panic(err.Error())
	}

	// read the SQL script file
	b, err := ioutil.ReadFile("../dataset_gps.sql")
	if err != nil {
		log.Fatal(err)
	}
	// execute the SQL statements
	_, err = mysqlDatabase.Exec(string(b))
	if err != nil {
		log.Fatal(err)
	}
	if proposer == ServerId(ServerID) {
		//defer sqliteDatabase.Close() // Defer Closing the database
		go runAsProposer(proposer)
	} else {
		proposerLookup.Lock()
		for i := 0; i < NOP; i++ {
			proposerLookup.m[Phase(i)] = proposer
		}
		proposerLookup.Unlock()
		//defer sqliteDatabase.Close() // Defer Closing the database
		go runAsValidator()
	}
}

func start() {
	takingInitRoles(ServerId(0))
}
