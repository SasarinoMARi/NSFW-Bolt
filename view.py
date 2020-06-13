import sys
from DBInterface import *
from MainWindow import *
from PyQt5.QtWidgets import QApplication 
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()

    app.exec_()

    DBInterface.distroy()
    sys.exit()