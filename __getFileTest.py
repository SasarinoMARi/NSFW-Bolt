import DBInterface
conn, c = DBInterface.establish()
files = DBInterface.getFiles(c)
for file in files:
    print(file.name)
DBInterface.distroy(conn)