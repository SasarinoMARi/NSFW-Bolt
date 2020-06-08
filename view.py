import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import dbInterface

class FileView(QWidget):
    defaultThumbnail = "thumb/sample.jpg"

    thumbnail = None
    name = None
    tags = None
    rate = None

    def __init__(self, root):
        super().__init__()
        layout = QGridLayout()

        background = QWidget()
        background.setStyleSheet('''
            background-image: url(./thumb/sample.jpg);
            background-position: center center;''')
        # bgEffect = QGraphicsEffect(background)
        # bgEffect.setOpacity(0.3)
        bgEffect = QGraphicsOpacityEffect()
        bgEffect.setOpacity(0.3)
        background.setGraphicsEffect(bgEffect)
        layout.addWidget(background, 0, 0)

        content = QHBoxLayout()

        self.thumbnail = QLabel(root)
        self.thumbnail.setFixedWidth(100)
        self.thumbnail.setFixedHeight(100)
        self.thumbnail.setMargin(0)
        self.setThumbnail(self.defaultThumbnail)
        content.addWidget(self.thumbnail)
        
        rightside = QVBoxLayout()        

        self.name = QLabel(root)
        self.name.setMargin(0)
        self.name.setFixedWidth(500)
        self.name.setFixedHeight(60)
        self.name.setWordWrap(True)
        f = self.name.font()
        f.setFamily('맑은 고딕')
        f.setPointSize(12)
        f.bold()
        self.name.setFont(f)
        rightside.addWidget(self.name)

        rightside.addStretch(1)
        
        self.rate = QLabel(root)
        f = self.rate.font()
        f.setFamily('맑은 고딕')
        f.setPointSize(10)
        self.rate.setFont(f)
        rightside.addWidget(self.rate)
        

        self.tags = QLabel(root)
        self.tags.setMargin(0)
        f = self.tags.font()
        f.setFamily('맑은 고딕')
        f.setPointSize(10)
        self.tags.setFont(f)
        rightside.addWidget(self.tags)

        content.addLayout(rightside)
        content.setSpacing(0)
        layout.addLayout(content, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.resize(100, 120)
        self.setLayout(layout)
        # self.setMinimumSize(100, 100)

    def setName(self, text):
        self.name.setText(text)
    
    def setRate(self, rate):
        self.rate.setText(f'Rate : {str(rate)} / 5')

    def setTags(self, tags):
        self.tags.setText(f'Tag : {", ".join(tags)}')
    
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

    def grid(self):
        conn, c = dbInterface.establish()
        files = dbInterface.getFiles(c)

        grid = QGridLayout()

        for column in range(int(len(files)/3)):
            for row in range(5):
                if(column*3+row >= len(files)): continue
                v = FileView(self)
                v.setText(files[column*3+row].name)
                grid.addWidget(v, column, row)

        content = QWidget()
        content.setLayout(grid)

        scrollView = QScrollArea()
        scrollView.setWidget(content)

        root = QHBoxLayout()
        root.addWidget(scrollView)

        self.setLayout(root)
        dbInterface.distroy(conn)

    def list(self):
        conn, c = dbInterface.establish()
        files = dbInterface.getFiles(c)

        li = QVBoxLayout()
        li.setContentsMargins(0, 0, 0, 0)

        for i in range(len(files)):
                v = FileView(self)
                v.setName(files[i].name)
                v.setRate(files[i].rate)
                v.setTags(files[i].tags)
                li.addWidget(v)

        content = QWidget()
        content.setLayout(li)

        scrollView = QScrollArea()
        scrollView.setWidget(content)

        root = QHBoxLayout()
        root.addWidget(scrollView)

        self.setLayout(root)
        dbInterface.distroy(conn)

    def initUI(self):
        self.setWindowTitle('NSFW Bolt')
        self.resize(700, 600)
        self.center()
        self.list()
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())