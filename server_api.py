from flask import Flask, jsonify, request, render_template
from server_logic import Server
import sqlite3
import argparse
import os

app = Flask(__name__)
logic=Server(app)
app.config['address'] = {
    0:('http://127.0.0.1', '9860'),
    1:('http://127.0.0.1', '9861'),
    2:('http://127.0.0.1', '9862'),
    3:('http://127.0.0.1', '9863'),
    4:('http://127.0.0.1', '9864'),
    5:('http://127.0.0.1', '9865')
}

def init_db():
    dbname = f"database_{app.config['id']}.db"
    try:
        connection = sqlite3.connect(dbname)

        with open('schema.sql') as f:
            connection.executescript(f.read())
            
        cur = connection.cursor()

        connection.commit()
        connection.close()
    except:
        os.remove(dbname)
        init_db()

def get_db_connection():
    dbname = f"database_{app.config['id']}.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn

def insert_dummy_data():
    conn=get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO backup_data VALUES (?, ?, ?)', (None, 'abc', 'def'))
    c.execute('INSERT INTO backup_data VALUES (?, ?, ?)', (None, 'ghi', 'jkl'))
    conn.commit()
    conn.close()
    
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return True

@app.route('/read', methods=['GET'])
def read_data():
    conn = get_db_connection()
    query =request.json['query']
    status, res = logic.on_requested_read(query, conn)
    conn.close()
    return jsonify({'status': status, 'data':res})


@app.route('/choose_backup', methods=['POST'])
def choose_backup():
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
    conn = get_db_connection()
    if not app.config['is_proposer']:
       return jsonify({'status': 'Failed: end point needs to belong to a proposer'})
    data = request.json
    res = logic.on_end_of_booth(data, conn)
    conn.close()
    return '', 200
    
@app.route('/update_backup_list', methods=['POST'])
def update_backup_list():
    chosen_list = request.json
    logic.update_backup_list(chosen_list)
    return '',200

@app.route('/delete_obsolete', methods=['POST'])
def delete_obsolete():
    backup_list = request.json['data']
    conn = get_db_connection()
    logic.on_requested_delete_obsolete(backup_list=backup_list, conn=conn)

@app.route('/data', methods=['POST'])
def add_user():
    foo = request.json['foo']
    bar = request.json['bar']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data (foo, bar) VALUES (?, ?)", (foo, bar))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': user_id, 'foo': foo, 'bar': bar}), 201

if __name__ == '__main__':        

    # Create the argument parser
    parser = argparse.ArgumentParser(description='Description of your program')

    # Add arguments
    parser.add_argument('--is_proposer', type=bool, help='Is this instance proposer or not')
    parser.add_argument('--id', type=int, help='A unique id for the instance')
    parser.add_argument('--log_file', type=str, help='Path to the log file')
    parser.add_argument('--port', type=str, help='Port number')
    parser.add_argument('--k_backups', type=int, help='The minimum number of backup dbs in the system')
    

    # Parse the arguments
    args = parser.parse_args()

    # Access the values of the arguments
    app.config['is_proposer'] = args.is_proposer
    app.config['is_backup'] = not args.is_proposer
    app.config['id'] = args.id
    app.config['log_file'] = args.log_file
    app.config['k_backups'] = args.k_backups
    app.config['port']=args.port
    
    init_db()
    insert_dummy_data()
    app.run(debug=True,port=args.port)