import os, sys, hashlib
import nFile
from DBInterface import *

def hash_file(filename):
   # make a hash object
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()

def addFile(path):
    if not os.path.exists(path):
        print("file or directory [" + path + "] does not exist.")
        return

    file = nFile()
    file.directory = os.path.dirname(path).replace('\'', '\'\'')
    file.isFolder = os.path.isdir(path)
    file.extension = None
    if not file.isFolder:
        sTemp = os.path.splitext(os.path.basename(path))
        if len(sTemp) >= 2:
            if len(sTemp[1]) >= 2:
                file.extension = sTemp[1][1:]
        # file.hash = hash_file(path) # 성능 때문에 비활성화
    
    file.name = os.path.basename(path).replace('\'', '\'\'')
    if file.extension != None: file.name = file.name[:-(len(file.extension)+1)]

    file.fileName = file.name

    print(file)
    DBInterface.instance().addFile({
        "name" : file.name,
        "filename" : file.fileName,
        "directory" : file.directory,
        "isFolder" : file.isFolder,
        "extension" : file.extension,
        "hash" : file.hash
    })


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        pass
    else:
        try:
            for i in range(len(sys.argv)-1):
                addFile(sys.argv[i+1])
                print(f"added [{i+1}/{len(sys.argv)-1}]")        
        except:
            print("Error:", sys.exc_info()[0])
            input()