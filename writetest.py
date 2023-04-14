import requests
import time
import mysql

addr = 'http://127.0.0.1:9860'

def get_db_connection():
    dbname = f"database_0"
    mydbconnection = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="123",
        database=dbname
    )

    return mydbconnection

def test_write():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"insert into gps_data (boothid, timestamp) values ({1},{time.now()})")
    conn.commit()
    conn.close()

    requests.get(f'{addr}/on_end_of_booth', data={'participants': [1,5,4]})

test_write()
    