import dbInterface
conn, c = dbInterface.establish()
files = dbInterface.getFiles(c)
for file in files:
    print(file.name)