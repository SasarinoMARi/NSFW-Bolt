import sys
import shutil
from DBInterface import *
from MainWindow import *
from PyQt5.QtWidgets import QApplication 
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    app.exec_()
    shutil.copy('bolt.db', 'bolt.db.bak') # Commit 전 복사
    # DBInterface.distroy()
    sys.exit()