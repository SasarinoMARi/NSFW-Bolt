import sys
import DBInterface
from MainWindow import *
from PyQt5.QtWidgets import QApplication 
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    conn, cur = DBInterface.establish()
    ex = MainWindow(cur)

    app.exec_()

    DBInterface.distroy(conn)
    sys.exit()