import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import dbInterface

class FileView(QVBoxLayout):
    defaultThumbnail = "thumb/sample.jpg"

    thumbnail = None
    label = None

    def __init__(self, root):
        super().__init__()

        self.thumbnail = QLabel(root)
        self.thumbnail.resize(100, 100)
        self.setThumbnail(self.defaultThumbnail)
        self.addWidget(self.thumbnail)
        
        self.label = QLabel(root)
        f = self.label.font()
        f.setFamily('맑은 고딕')
        f.setPointSize(15)
        self.label.setFont(f)
 
        # self.resize(100, 120)
        self.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)
    
    def setThumbnail(self, thumbnailPath):
        p = QPixmap(thumbnailPath)
        p = p.scaled(100, 100)
        self.thumbnail.setPixmap(p)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def label(self):
        conn, c = dbInterface.establish()
        files = dbInterface.getFiles(c)

        grid = QGridLayout()

        for column in range(int(len(files)/3)):
            for row in range(5):
                print(f'{column*3+row} / {len(files)}')
                if(column*3+row >= len(files)): continue

                v = FileView(self)
                v.setText(files[column*3+row].name)
                grid.addLayout(v, column, row)


        scrollView = QScrollArea()
        scrollView.setLayout(grid)

        root = QHBoxLayout()
        root.addWidget(scrollView)

        self.setLayout(root)
        dbInterface.distroy(conn)


    def initUI(self):
        self.setWindowTitle('NSFW Bolt')
        self.resize(800, 600)
        self.center()
        self.label()
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())