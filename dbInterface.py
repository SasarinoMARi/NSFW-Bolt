__fn = 'kindan.db'
import sqlite3
import datetime
from collections import namedtuple

def establish():
    conn = sqlite3.connect(__fn)
    return conn, conn.cursor()

def distroy(connection):
    connection.commit()
    connection.close()

def initializeTables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Files(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            directory TEXT NOT NULL,
            isFolder BOOLEAN NOT NULL)''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Rates(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            fidx INTEGER,
            rate INTEGER NOT NULL,
            
            FOREIGN KEY(fidx) REFERENCES Files(idx))''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tag(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            fidx INTEGER,
            name TEXT NOT NULL, 

            FOREIGN KEY(fidx) REFERENCES Files(idx))''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tags(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            fidx INTEGER,
            tidx INTEGER,
            
            FOREIGN KEY(fidx) REFERENCES Files(idx),
            FOREIGN KEY(tidx) REFERENCES Tag(idx))''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Exetensions(
            exetension TEXT PRIMARY KEY,
            process TEXT NOT NULL)''')

def insert(cursor, data):
    sql = f'''INSERT INTO Files(name, path) VALUES(
        '{data[0]}','{data[1]}')'''
    cursor.execute(sql)

def show(cursor):
    sql = '''SELECT * FROM Files'''
    for row in cursor.execute(sql):
        print(row)

def sampleData():
    return "name", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def test() :
    data = sampleData()
    connection, cursor = establish()
    initializeTables(cursor)
    # insert(cursor, data)
    show(cursor)
    distroy(connection)

test()