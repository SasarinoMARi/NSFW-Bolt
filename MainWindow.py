import os
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import add
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
        index = self.getSelectedFileIndex()
        filter = self.wSearchBar.text().split(',') if not self.wSearchBar is None else []
        self.files = DBInterface.instance().getFiles(filter)
        self.model = FileModel(self, self.files)
        self.wListView.setModel(self.model)
        if index != None: self.selectItem(index)

    def getSelectedFileIndex(self):
        idxes = self.wListView.selectedIndexes()
        if len(idxes) == 0: return None
        return idxes[0].row()

    def getSelectedFile(self):
        idx = self.getSelectedFileIndex()
        if idx is None: return None
        item = self.files[idx]
        print(f'Selected File: {item.name}')
        return DBInterface.getFile(item.index) # 왜 이렇게 슬픈 코드가 되었는지는 DbInterface.getFiles 참고..

    def initUIListView(self):
        self.wListView = QListView(self)
        self.wListView.setItemDelegate(FileModelDelegate(self))
        self.wListView.setMinimumWidth(400)
        self.wListView.setMinimumHeight(200)
        self.loadFilesFromDB()

        return self.wListView

    def selectItem(self, index):
        index = self.model.index(index)
        self.wListView.setCurrentIndex(index)

    def initUIButtons(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        def showDetailWindow():
            file = self.getSelectedFile()
            path = os.path.realpath(os.path.join(file.directory, file.fileName))
            if file.extension != None and file.extension != 'None': path+=f'.{file.extension}'
            if os.path.exists(path): os.startfile(path)
            else: QMessageBox.critical(self, "Error", f"Cannot find File or Directory:\n\n{path}")

        buttonDetail = QPushButton()
        buttonDetail.setText("Open")
        buttonDetail.setFixedHeight(40)
        buttonDetail.clicked.connect(showDetailWindow)

        def showRateWindow():
            file = self.getSelectedFile()
            win = RateWindow(file)
            result = win.showModal()
            if result:
                rate = win.currentRate
                print(f"set rate to {rate}..")
                DBInterface.instance().setRate(file.index, rate)
                self.loadFilesFromDB()

        buttonRate = QPushButton()
        buttonRate.setText("Set Rate")
        buttonRate.setFixedHeight(40)
        buttonRate.clicked.connect(showRateWindow)

        def showTagEditWindow():
            file = self.getSelectedFile()
            win = TagWindow(file)
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
        buttonTag.setFixedHeight(40)
        buttonTag.clicked.connect(showTagEditWindow)


        def onRandomButtonClick():
            index = random.randrange(len(self.files))
            self.selectItem(index)

        buttonRandom = QPushButton()
        buttonRandom.setText("Random")
        buttonRandom.setFixedHeight(40)
        buttonRandom.clicked.connect(onRandomButtonClick)


        def onAddButtonClick():
            win = AddFileWindow()
            result = win.showModal()
            if result:
                newPaths = win.getResult()
                for path in newPaths:
                    add.addFile(path)
                self.loadFilesFromDB()

        buttonAdd = QPushButton()
        buttonAdd.setText("Add")
        buttonAdd.setFixedHeight(40)
        buttonAdd.clicked.connect(onAddButtonClick)

        def onDeleteButtonClick():
            file = self.getSelectedFile()
            result = QMessageBox.question(self, "Confirm", f"Delete file from NSFW-Bolt?\nReal file is does not delete.\n\n{file.name}", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                DBInterface.instance().deleteFile(file.index)
                self.loadFilesFromDB()

        buttonDelete = QPushButton()
        buttonDelete.setText("Delete")
        buttonDelete.setFixedHeight(40)
        buttonDelete.clicked.connect(onDeleteButtonClick)


        layout.addWidget(buttonDetail)
        layout.addWidget(buttonRate)
        layout.addWidget(buttonTag)
        layout.addSpacing(20)
        layout.addWidget(buttonRandom)
        layout.addSpacing(20)
        layout.addWidget(buttonAdd)
        layout.addWidget(buttonDelete)

        return layout

    def initUISearchBar(self):
        self.wSearchBar = QLineEdit()

        def searchTextChanged():
            self.loadFilesFromDB()
            
        self.wSearchBar.textChanged.connect(searchTextChanged)
        self.wSearchBar.setPlaceholderText("Enter ketword.. (Separate with commas(,). tag:[Tag Name], rate:[Rate]")
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