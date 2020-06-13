from DBInterface import *
files = DBInterface.instance().getFiles()
for file in files:
    print(file.name)
del DBInterface.instance