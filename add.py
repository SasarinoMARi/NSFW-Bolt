import os
import sys
from DBInterface import *

def addFile(path):
    if not os.path.exists(path):
        print("file or directory [" + path + "] does not exist.")
        return

    name = os.path.splitext(os.path.basename(path))[0]
    directory = os.path.dirname(path)
    isFolder = os.path.isdir(path)
    extension = None
    if not isFolder:
        sTemp = os.path.splitext(path)
        if len(sTemp) >= 2:
            if len(sTemp[1]) >= 2:
                extension = sTemp[1][1:]

    DBInterface.instance().addFile({
        "name" : name,
        "filename" : name,
        "directory" : directory,
        "isFolder" : isFolder,
        "extension" : extension
    })

if len(sys.argv) <= 1:
    pass
else:
    for i in range(len(sys.argv)-1):
        print(f"added [{i+1}/{len(sys.argv)-1}]")
        addFile(sys.argv[i+1])

input("작업이 완료되었습니다. 아무 키나 눌러주세요.")