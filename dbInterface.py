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
        # self.establish()
    
    def __del__(self):
        # self.distroy()
        pass

    # 에러 났을 때 데이터 다 날아가서 빡치는바람에 이렇게함
    def __establish(self):
        self.establish()
    
    def __distroy(self):
        self.distroy()

    def __printSqlLog(self, sql):
        sql = "\n\t" + sql.replace("\n", "")
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
        # Cascade 연쇄삭제 왜 안되는지 아는사람? ㅠㅠ 솔직히 냅둬도 상관없으니까 못본체하겠음
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Files(idx INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, filename TEXT NOT NULL, directory TEXT NOT NULL, isFolder BOOLEAN NOT NULL, extension TEXT, thumbnail TEXT, hash TEXT, serialNumber TEXT)''')
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Rates(idx INTEGER PRIMARY KEY AUTOINCREMENT, fidx INTEGER, rate INTEGER NOT NULL, FOREIGN KEY(fidx) REFERENCES Files(idx) ON DELETE CASCADE)''')
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Tag(idx INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)''')
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Tags(idx INTEGER PRIMARY KEY AUTOINCREMENT, fidx INTEGER, tidx INTEGER, FOREIGN KEY(fidx) REFERENCES Files(idx) ON DELETE CASCADE, FOREIGN KEY(tidx) REFERENCES Tag(idx) ON DELETE CASCADE)''')
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS Exetensions(exetension TEXT PRIMARY KEY, process TEXT NOT NULL)''')

    # 새 파일 추가
    def addFile(self, data):
        self.__establish()
        if data['extension'] is None: data['extension'] = 'NULL'
        else: data['extension'] = f"'{data['extension']}'"

        sql = f'''INSERT INTO Files(name, filename, directory, isFolder, extension) VALUES(
            '{data['name']}','{data['name']}','{data['directory']}', {data['isFolder']}, {data['extension']})'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        self.__distroy()
        
    #  인덱스로 파일 조회
    def getFile(self, idx):
        self.__establish()
        sql = f'''SELECT F.idx, F.name, F.filename, F."directory", F.isFolder, F.extension, F.thumbnail, F.serialNumber, F.hash, R.rate, GROUP_CONCAT(Tag.name, ',') AS 'tagNames', GROUP_CONCAT(Tag.idx, ',') AS 'tagIds' FROM Files AS F LEFT JOIN Tags AS T ON T.fidx is F.idx LEFT JOIN Tag ON T.tidx IS Tag.idx LEFT JOIN Rates AS R ON R.fidx is F.idx WHERE F.idx is {idx} GROUP BY F.idx '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        
        for item in result:
            return nFile.createWithRow(item)
        self.__distroy()
        return None

    # 등록된 파일 조회
    def getFiles(self, filters=[], operator="AND") :
        self.__establish()
        sql = f'''SELECT F.idx, F.name, F.filename, F."directory", F.isFolder, F.extension, F.thumbnail, F.serialNumber, F.hash, R.rate, GROUP_CONCAT(Tag.name, ',') AS 'tagNames', GROUP_CONCAT(Tag.idx, ',') AS 'tagIds' FROM Files AS F LEFT JOIN Tags AS T ON T.fidx is F.idx LEFT JOIN Tag ON T.tidx IS Tag.idx LEFT JOIN Rates AS R ON R.fidx is F.idx'''
        if len(filters) > 0: sql += ' ' + 'WHERE'
        for i in range(len(filters)):
            filter = filters[i].strip()
            if len(filter) > 4 and filter.lower().startswith('tag:'): # 태그 필터
                sql += ' ' + f''' Tag.name LIKE '%{filter[4:]}%' ''' # group_concat을 대상으로 where절 실행시 오류남.. ㅠ
            elif len(filter) > 5 and filter.lower().startswith('rate:'): # 별점 필터
                f = filter[5:6]
                if not f.isdigit(): continue
                sql += ' ' +  f''' R.rate >= {f} '''
            elif len(filter) > 10 and filter.lower().startswith('extension:'): # 별점 필터
                sql += ' ' + f''' F.extension LIKE '%{filter[10:]}%' ''' # group_concat을 대상으로 where절 실행시 오류남.. ㅠ
            else : # 제목 필터
                sql += ' ' + f''' F.name LIKE '%{filter}%' '''

            if i+1 < len(filters): sql += ' ' + operator
        sql += ''' GROUP BY F.idx ORDER BY F.name'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)

        files = []
        for item in result:
            f = nFile.createWithRow(item)
            files.append(f)
        self.__distroy()
        return files

    def setFileName(self, idx, name):
        self.__establish()
        sql = f'''UPDATE Files SET name = '{name}' WHERE idx IS {idx}'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'File [{idx}] name was changed to {name}.')
        self.__distroy()

    def deleteFile(self, fidx):
        self.__establish()
        sql = f'''DELETE FROM files WHERE idx is {fidx}'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'File [{fidx}] was deleted.')
        self.__distroy()

    # 별점 추가
    def setRate(self, id, rate):
        self.__establish()
        self.removeRate(id)

        sql = f'''INSERT INTO Rates(fidx, rate) VALUES(
            '{id}',{rate})'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Set rate of [{id}] to {rate}')
        self.__distroy()

    # 별점 삭제
    def removeRate(self, id):
        self.__establish()
        sql = f'''DELETE FROM Rates WHERE fidx IS '{id}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Delete rate of [{id}]')
        self.__distroy()
        

    # 태그 추가
    def addTag(self, name):
        self.__establish()
        sql = f'''INSERT INTO Tag(name) VALUES(
            '{name}')'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Tag [{name}] added. {result}')
        self.__distroy()

    # 태그 조회
    def getTags(self):
        self.__establish()
        sql = f'''SELECT * FROM Tag'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)

        tags = []
        for item in result:
            tags.append(nTag.createWithRow(item))
        self.__distroy()
        return tags

    # 태그 이름으로 인덱스 조회
    def getTag(self, name):
        self.__establish()
        sql = f'''SELECT * FROM Tag WHERE name = '{name}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        
        for item in result:
            return item
        self.__distroy()
        return None

    # 태그 삭제
    def removeTag(self, id):
        self.__establish()
        sql = f'''DELETE FROM Tag WHERE idx IS '{id}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Tag [{id}] deleted. {result}')
        self.__distroy()

    # 태그 삭제
    def removeTagWithName(self, name):
        self.__establish()
        sql = f'''DELETE FROM Tag WHERE name IS '{name}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Tag [{name}] deleted. {result}')
        self.__distroy()


    # 파일에 태그 추가
    def addTagFileTag(self, id, tagId):
        self.__establish()
        sql = f'''INSERT INTO Tags(fidx, tidx) VALUES(
            '{id}','{tagId}')'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Added tag {tagId} to [{id}]')
        self.__distroy()

    # 파일에 태그 삭제
    def removeFileTag(self, id, tagId):
        self.__establish()
        sql = f'''DELETE FROM Tags WHERE fidx IS '{id}' AND tidx IS '{tagId}' '''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'Deleted tag {tagId} from [{id}]')
        self.__distroy()

        
    # 확장자 추가
    def addExtensions(self, exetension, process):
        self.__establish()
        sql = f'''INSERT INTO Exetensions(exetension, process) VALUES(
            '{exetension}','{process}')'''
        self.__printSqlLog(sql)
        result = self.connection.cursor().execute(sql)
        print(f'extension {exetension} added. {result}')
        self.__distroy()

    # def show(self):
    #     sql = '''SELECT * FROM Files'''
    #     for row in self.connection.cursor().execute(sql):
    #         print(row)

    # def sampleData(self):
    #     return "name", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

DBInterface = DBInterface.instance()