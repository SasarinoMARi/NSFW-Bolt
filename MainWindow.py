from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from DBInterface import *
from nFile import *
from DialogWindows import *

class MainWindow(QWidget):
    wListView = None
    wSearchBar = None

    files = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def setPositionToCenterOfScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 서순: 반드시 initUIListView 호출 이후 호출되어야 함.
    def loadFilesFromDB(self):
        filter = self.wSearchBar.text() if not self.wSearchBar is None else ""
        self.files = DBInterface.instance().getFiles(filter)
        model = FileModel(self, self.files)
        self.wListView.setModel(model)

    # nFile 인스턴스와 list에서의 index 반환
    def getSelectedFile(self):
        idxes = self.wListView.selectedIndexes()
        if len(idxes) == 0: return None, None
        idx = idxes[0].row()
        item = self.files[idx]
        print(f'Selected File: {item.name}')
        return item, idx

    def initUIListView(self):
        self.wListView = QListView(self)
        self.wListView.setItemDelegate(FileModelDelegate(self))
        self.loadFilesFromDB()

        return self.wListView

    def initUIButtons(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        def showDetailWindow():
            file = self.getSelectedFile()

        buttonDetail = QPushButton()
        buttonDetail.setText("Detail")
        buttonDetail.clicked.connect(showDetailWindow)

        def showRateWindow():
            file, idx = self.getSelectedFile()
            win = RateWindow(file, idx)
            result = win.showModal()
            if result:
                rate = win.currentRate
                print(f"set rate to {rate}..")
                DBInterface.instance().setRate(file.index, rate)
                self.loadFilesFromDB()

        buttonRate = QPushButton()
        buttonRate.setText("Set Rate")
        buttonRate.clicked.connect(showRateWindow)

        def showTagEditWindow():
            file, idx = self.getSelectedFile()
            win = TagWindow(file, idx)
            result = win.showModal()
            if result:
                newIds, deletedIds = win.getResult()
                for id in newIds:
                    DBInterface.instance().addTagFileTag(file.index, id)
                for id in deletedIds:
                    DBInterface.instance().removeFileTag(file.index, id)
                self.loadFilesFromDB()

        buttonTag = QPushButton()
        buttonTag.setText("Edit Tag")
        buttonTag.clicked.connect(showTagEditWindow)

        layout.addWidget(buttonDetail)
        layout.addWidget(buttonRate)
        layout.addWidget(buttonTag)

        self.lButtons = layout
        return layout

    def initUISearchBar(self):
        self.wSearchBar = QLineEdit()

        def searchTextChanged():
            self.loadFilesFromDB()
            
        self.wSearchBar.textChanged.connect(searchTextChanged)
        return self.wSearchBar

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