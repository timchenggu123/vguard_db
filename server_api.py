from flask import Flask, jsonify, request, render_template
from server_logic import Server
import sqlite3
import sys
import argparse

app = Flask(__name__)

def init_db():
    dbname = f"database_{app.config['id']}.db"
    connection = sqlite3.connect(dbname)

    with open('schema.sql') as f:
        connection.executescript(f.read())
        
    cur = connection.cursor()

    connection.commit()
    connection.close()

def get_db_connection():
    dbname = f"database_{app.config['id']}.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return True

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        data.append({'id': row[0], 'foo': row[1], 'bar': row[2]})
    return jsonify({'data': data})

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
    

    # Parse the arguments
    args = parser.parse_args()

    # Access the values of the arguments
    app.config['is_proposer'] = args.is_proposer
    app.config['is_backup'] = not args.is_proposer
    app.config['id'] = args.id
    app.config['log_file'] = args.log_file
    server_logic=Server(app)
    app.config['logic']=server_logic
    init_db()
    app.run(debug=True)