import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import dbInterface
from nFile import *

class MyApp(QWidget):

    files = None
    selectedIdx = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _makeGrid(self):
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

    def makeList(self):
        conn, c = dbInterface.establish()
        files = dbInterface.getFiles(c)

        view = QListView(self)
        model = FileModel(self, files)
        view.setModel(model)
        view.setItemDelegate(FileModelDelegate(self))

        dbInterface.distroy(conn)

        return view

    def _makeScroll(self):
        conn, c = dbInterface.establish()
        self.files = dbInterface.getFiles(c)

        li = QVBoxLayout()
        li.setContentsMargins(0, 0, 0, 0)
  
        for i in range(len(self.files)):
            view = FileView(self, self.files[i])
            # def onClick(self, e):
                # self.selectedIdx = i
                # print(f'selectedIdx : {self.selectedIdx}')
            # view.mouseReleaseEvent(onClick)
            li.addWidget(view)

        content = QWidget()
        content.setLayout(li)

        scrollView = QScrollArea()
        scrollView.setWidget(content)
        scrollView.setMinimumSize(700, 400)
        scrollView.setFixedWidth(700)

        dbInterface.distroy(conn)

        return scrollView
    
    def makeButton(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        buttonDetail = QPushButton()
        buttonDetail.setText("Detail")
        
        buttonDetail.clicked.connect(lambda: print(self.files[0]))

        buttonRate = QPushButton()
        buttonRate.setText("Set Rate")

        buttonTag = QPushButton()
        buttonTag.setText("Edit Tag")

        layout.addWidget(buttonDetail)
        layout.addWidget(buttonRate)
        layout.addWidget(buttonTag)

        return layout

    def initUI(self):
        self.setWindowTitle('NSFW Bolt')
        self.resize(700, 600)
        self.center()
        root = QHBoxLayout()
        li = self.makeList()
        root.addWidget(li)
        buttonView = self.makeButton()
        root.addLayout(buttonView)
        self.setLayout(root)
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())