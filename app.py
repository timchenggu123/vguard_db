from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

def get_db_connection():
    conn = sqlite3.connect('database.db')
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
    app.run(debug=True)