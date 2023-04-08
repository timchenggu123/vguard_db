from flask import Flask, jsonify, request, render_template
from server_logic import Server
import sqlite3
import argparse
import os
import json
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
logic=Server(app)
app.config['address'] = {
    0:('http://127.0.0.1', '9860'),
    1:('http://127.0.0.1', '9861'),
    2:('http://127.0.0.1', '9862'),
    3:('http://127.0.0.1', '9863'),
    4:('http://127.0.0.1', '9864'),
    5:('http://127.0.0.1', '9865'),
    6:('http://127.0.0.1', '9866') 
}


#def init_db():
#    dbname = f"database_{app.config['id']}.db"
 #   try:
#        connection = sqlite3.connect(dbname)
#
#        with open('dataset_gps.sql') as f:
#            connection.executescript(f.read())
#
#        connection.commit()
#        connection.close()
 #   except:
 #       os.remove(dbname)
 #       init_db()

def init_db():
    dbname = f"database_{app.config['id']}"
    try:
        mydbconnection = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="123"
        )
        # Create a new database if it does not exist
        mycursor = mydbconnection.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS "+dbname)
        mycursor.execute("USE " + dbname)
        mydbconnection.commit()
        mydbconnection.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def check_offline():
    if logic.offline:
        raise TypeError()
    
def get_db_connection():
    #conn = sqlite3.connect(dbname)
    #conn.row_factory = sqlite3.Row
    dbname = f"database_{app.config['id']}"
    mydbconnection = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="123",
        database=dbname
    )

    return mydbconnection

def insert_dummy_data():
    conn=get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO backup_data VALUES (?, ?, ?)', (None, 'abc', 'def'))
    c.execute('INSERT INTO backup_data VALUES (?, ?, ?)', (None, 'ghi', 'jkl'))
    conn.commit()
    conn.close()
    
@app.route('/read', methods=['GET'])
def read_data():
    check_offline()
    conn = get_db_connection()
    query =request.json['query']
    data, new_backup_ids = logic.on_requested_read(query, conn)
    conn.close()
    return jsonify({'new_backup_ids': new_backup_ids, 'data': data}), 200


@app.route('/choose_backup', methods=['POST'])
def choose_backup():
    check_offline()
    conn = get_db_connection()
    data = request.json
    res = logic.on_chosen_as_backup(data, conn)
    conn.close()
    if res:
        return '',200
    else:
        return '',201

@app.route('/end_of_booth', methods=['Get'])
def end_of_booth():
    check_offline()
    conn = get_db_connection()
    if not app.config['is_proposer']:
       return jsonify({'status': 'Failed: end point needs to belong to a proposer'})
    data = request.json
    logic.on_end_of_booth(data, conn)
    conn.close()
    return '', 200
    
@app.route('/update_backup_list', methods=['POST'])
def update_backup_list():
    check_offline()
    chosen_list = request.json
    logic.update_backup_list(chosen_list)
    return '',200

@app.route('/delete_obsolete', methods=['POST'])
def delete_obsolete():
    check_offline()
    backup_list = request.json
    conn = get_db_connection()
    logic.on_requested_delete_obsolete(backup_list=backup_list, conn=conn)
    conn.close()
    return '', 200

########Debugging endpoints###############
@app.route('/')
def index():
    conn = get_db_connection()
    data = logic._db_read_all(conn, 'gps_data')
    conn.close()
    return jsonify({"data":data}),200

@app.route('/trigger_read')
def trigger_read():
    query = 'select * from gps_data'
    data =logic.read_data(query)
    return jsonify({'data':data}), 200

@app.route('/trigger_insert_dummy')
def trigger_insert_dummy():
    insert_dummy_data()
    return jsonify({}), 200

@app.route('/set_offline')
def set_offline():
    logic.offline=True
    return jsonify({}), 200
    
@app.route('/set_online')
def set_online():
    logic.offline=False
    return jsonify({}), 200

if __name__ == '__main__':        

    # Create the argument parser
    parser = argparse.ArgumentParser(description='Description of your program')

    # Add arguments
    parser.add_argument('--is_proposer', type=bool, help='Is this instance proposer or not')
    parser.add_argument('--id', type=int, help='A unique id for the instance')
    parser.add_argument('--log_file', type=str, help='Path to the log file')
    parser.add_argument('--port', type=str, help='Port number')
    parser.add_argument('--k_backups', type=int, help='The minimum number of backup dbs in the system')
    parser.add_argument('--proposer_id', type=int, help='The id of the proposer', default=0) 
    parser.add_argument('--debug', type=bool, help='Set true to activate debug mode', default = True)
    parser.add_argument('--address_file', type=str, help='Path to the address file', default = 'address.json')

    # Parse the arguments
    args = parser.parse_args()

    # Access the values of the arguments
    app.config['is_proposer'] = args.is_proposer
    app.config['is_backup'] = not args.is_proposer
    app.config['id'] = args.id
    app.config['log_file'] = args.log_file
    app.config['k_backups'] = args.k_backups
    app.config['port']=args.port
    app.config['proposer_id']=args.proposer_id
    app.config['debug']=args.debug
    if args.address_file:
        app.config['address'] = json.load(open(args.address_file))
    
    init_db()
    # insert_dummy_data()

    app.run(debug=True,port=args.port)