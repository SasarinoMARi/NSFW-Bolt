__fn = 'bolt.db'
import sqlite3
import datetime
from collections import namedtuple

def establish():
    conn = sqlite3.connect(__fn)
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def distroy(connection):
    connection.commit()
    connection.close()

def initializeTables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Files(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            filename TEXT NOT NULL,
            directory TEXT NOT NULL,
            isFolder BOOLEAN NOT NULL,
            extension TEXT,
            thumbnail TEXT)''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Rates(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            fidx INTEGER,
            rate INTEGER NOT NULL,
            
            FOREIGN KEY(fidx) REFERENCES Files(idx))''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tag(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tags(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            fidx INTEGER,
            tidx INTEGER,
            
            FOREIGN KEY(fidx) REFERENCES Files(idx),
            FOREIGN KEY(tidx) REFERENCES Tag(idx))''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS Exetensions(
            exetension TEXT PRIMARY KEY,
            process TEXT NOT NULL)''')

# 새 파일 추가
def addFile(cursor, data):
    if data['extension'] is None: data['extension'] = 'NULL'
    else: data['extension'] = f"'{data['extension']}'"

    sql = f'''INSERT INTO Files(name, filename, directory, isFolder, extension) VALUES(
        '{data['name']}','{data['name']}','{data['directory']}', {data['isFolder']}, {data['extension']})'''
    result = cursor.execute(sql)
    
from nFile import *
def getFiles(cursor) :
    sql = f'''SELECT * from Files'''
    result = cursor.execute(sql)

    files = []
    for item in result:
        f = nFile.createWithRow(item)
        files.append(f)
    return files

# 별점 추가
def setRate(cursor, id, rate):
    sql = f'''INSERT INTO Rates(fidx, rate) VALUES(
        '{id}','{rate}')'''
    result = cursor.execute(sql)
    print(result)

# 별점 삭제
def removeTag(cursor, id):
    sql = f'''DELETE FROM Rates WHERE fidx IS '{id}')'''
    result = cursor.execute(sql)
    print(result)
    

# 태그 추가
def addTag(cursor, name):
    sql = f'''INSERT INTO Tag(name) VALUES(
        '{name}')'''
    result = cursor.execute(sql)
    print(result)

# 태그 삭제
def removeTag(cursor, name):
    sql = f'''DELETE FROM Tag WHERE name IS '{name}')'''
    result = cursor.execute(sql)
    print(result)


# 파일에 태그 추가
def setTag(cursor, id, tagId):
    sql = f'''INSERT INTO Tags(fidx, tidx) VALUES(
        '{id}','{tagId}')'''
    result = cursor.execute(sql)
    print(result)

# 파일에 태그 삭제
def removeTag(cursor, id, tagId):
    sql = f'''DELETE FROM Tags WHERE fidx IS '{id}' AND tidx IS '{tagId}'')'''
    result = cursor.execute(sql)
    print(result)

    
# 확장자 추가
def addExtensions(cursor, exetension, process):
    sql = f'''INSERT INTO Exetensions(exetension, process) VALUES(
        '{exetension}','{process}')'''
    result = cursor.execute(sql)
    print(result)
    

# def show(cursor):
#     sql = '''SELECT * FROM Files'''
#     for row in cursor.execute(sql):
#         print(row)

# def sampleData():
#     return "name", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")