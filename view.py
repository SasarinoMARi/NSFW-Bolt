import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import dbInterface
from nFile import *

class MyApp(QWidget):
    wListView = None

    files = None
    dbCur = None

    def __init__(self, cur):
        super().__init__()
        self.dbCur = cur
        self.initUI()

    def setPositionToCenterOfScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 서순: 반드시 initUIListView 호출 이후 호출되어야 함.
    def loadFilesFromDB(self, keyword=""):
        self.files = dbInterface.getFiles(self.dbCur, keyword)
        model = FileModel(self, self.files)
        self.wListView.setModel(model)

    def initUIListView(self):
        self.wListView = QListView(self)
        self.wListView.setItemDelegate(FileModelDelegate(self))
        self.loadFilesFromDB()

        return self.wListView

    def initUIButtons(self):
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

        self.lButtons = layout
        return layout

    def initUISearchBar(self):
        wSearchBar = QLineEdit()

        def searchTextChanged(self):
            self.loadFilesFromDB(wSearchBar.text())
            
        wSearchBar.textChanged.connect(searchTextChanged)
        return wSearchBar

    def inflateLayout(self):
        root = QHBoxLayout()

        layout1_1 = QVBoxLayout()
        layout1_1.addWidget(self.initUISearchBar())
        layout1_1.addWidget(self.initUIListView())

        root.addLayout(layout1_1)
        root.addLayout(self.initUIButtons())
        return root

    def initUI(self):
        self.setWindowTitle('NSFW Bolt')
        self.resize(700, 600)
        self.setPositionToCenterOfScreen()
        self.setLayout(self.inflateLayout())
        self.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    conn, cur = dbInterface.establish()
    ex = MyApp(cur)

    app.exec_()

    dbInterface.distroy(conn)
    sys.exit()