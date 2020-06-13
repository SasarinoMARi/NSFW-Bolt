import sqlite3
import datetime
from collections import namedtuple

from nFile import *
from nTag import *

class __SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance

class DBInterface(__SingletonInstane):
    connection = None

    def __init__(self):
        super().__init__()
        self.establish()
    
    def __del__(self):
        self.distroy()

    def __printSqlLog(self, sql):
        sql = "\n\t" + sql.replace("\n", "").replace("  ", "")
        sql = sql.replace("FROM", "\n\tFROM")
        sql = sql.replace("WHERE", "\n\tWHERE")
        sql = sql.replace("GROUP BY", "\n\tGROUP BY")
        sql = sql.replace("ORDER BY", "\n\tORDER BY")
        print(f'Query:{sql}')

    def establish(self):
        print("Establish connection with local Database...")
        self.connection = sqlite3.connect('bolt.db')
        self.connection.row_factory = sqlite3.Row
        self.initializeTables()
        print("OK!")

    def distroy(self):
        print("Commit Database and close connection...")
        if not self.connection is None:
            self.connection.commit()
            self.connection.close()
        print("OK!")

    def initializeTables(self):
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Files(
                idx INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                filename TEXT NOT NULL,
                directory TEXT NOT NULL,
                isFolder BOOLEAN NOT NULL,
                extension TEXT,
                thumbnail TEXT)''')
                
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Rates(
                idx INTEGER PRIMARY KEY AUTOINCREMENT,
                fidx INTEGER,
                rate INTEGER NOT NULL,
                
                FOREIGN KEY(fidx) REFERENCES Files(idx))''')
                
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Tag(
                idx INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL)''')
                
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Tags(
                idx INTEGER PRIMARY KEY AUTOINCREMENT,
                fidx INTEGER,
                tidx INTEGER,
                
                FOREIGN KEY(fidx) REFERENCES Files(idx),
                FOREIGN KEY(tidx) REFERENCES Tag(idx))''')
                
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Exetensions(
                exetension TEXT PRIMARY KEY,
                process TEXT NOT NULL)''')

    # 새 파일 추가
    def addFile(self, data):
        if data['extension'] is None: data['extension'] = 'NULL'
        else: data['extension'] = f"'{data['extension']}'"

        sql = f'''INSERT INTO Files(name, filename, directory, isFolder, extension) VALUES(
            '{data['name']}','{data['name']}','{data['directory']}', {data['isFolder']}, {data['extension']})'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        
    # 등록된 파일 조회
    def getFiles(self, filter="") :
        sql = f'''SELECT F.idx, F.name, F.filename, F."directory", F.isFolder, F.extension, F.thumbnail, R.rate, GROUP_CONCAT(Tag.name, ',') AS 'Tags' FROM Files AS F LEFT JOIN Tags AS T ON T.fidx is F.idx LEFT JOIN Tag ON T.tidx IS Tag.idx LEFT JOIN Rates AS R ON R.fidx is F.idx WHERE F.name LIKE '%{filter}%' GROUP BY F.idx'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)

        files = []
        for item in result:
            f = nFile.createWithRow(item)
            files.append(f)
        return files

    # 별점 추가
    def setRate(self, id, rate):
        self.removeRate(id)

        sql = f'''INSERT INTO Rates(fidx, rate) VALUES(
            '{id}',{rate})'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Set rate of [{id}] to {rate}')

    # 별점 삭제
    def removeRate(self, id):
        sql = f'''DELETE FROM Rates WHERE fidx IS '{id}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Delete rate of [{id}]')
        

    # 태그 추가
    def addTag(self, name):
        sql = f'''INSERT INTO Tag(name) VALUES(
            '{name}')'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Tag [{name}] added. {result}')

    # 태그 조회
    def getTags(self):
        sql = f'''SELECT * FROM Tag'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)

        tags = []
        for item in result:
            tags.append(nTag.createWithRow(item))
        return tags

    # 태그 삭제
    def removeTag(self, name):
        sql = f'''DELETE FROM Tag WHERE name IS '{name}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Tag [{name}] deleted. {result}')


    # 파일에 태그 추가
    def setTagFileTag(self, id, tagId):
        sql = f'''INSERT INTO Tags(fidx, tidx) VALUES(
            '{id}','{tagId}')'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Added tag {tagId} to [{id}]')

    # 파일에 태그 삭제
    def removeFileTag(self, id, tagId):
        sql = f'''DELETE FROM Tags WHERE fidx IS '{id}' AND tidx IS '{tagId}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Deleted tag {tagId} to [{id}]')

        
    # 확장자 추가
    def addExtensions(self, exetension, process):
        sql = f'''INSERT INTO Exetensions(exetension, process) VALUES(
            '{exetension}','{process}')'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'extension {exetension} added. {result}')

    # def show(self):
    #     sql = '''SELECT * FROM Files'''
    #     for row in self.connection.cursor().execute(sql):
    #         print(row)

    # def sampleData(self):
    #     return "name", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

DBInterface = DBInterface.instance()