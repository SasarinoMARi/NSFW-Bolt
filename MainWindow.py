import os
import random
import shutil
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

        # 검색 연산자 계산
        if self.wSearchOptionAnd.isChecked() : operator = "AND"
        elif self.wSearchOptionOr.isChecked() : operator = "OR"
        else: operator = "AND"

        print(operator)

        self.files = DBInterface.instance().getFiles(filter, operator)
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

    def getFilePath(self, file):
        path = os.path.join(file.directory, file.fileName) 
        if file.extension != None and file.extension != 'None': path+=f'.{file.extension}'
        return path

    def initUIButtons(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        def openFile():
            file = self.getSelectedFile()
            if file is None: return
            path = self.getFilePath(file)
            if os.path.isdir(path):
                interFiles = os.listdir(path)
                if len(interFiles) > 0:
                    path = os.path.join(path, interFiles[0]) # 이 기능은 사용할지 말지 사용자가 정할 수 있게 해주자
            if os.path.exists(path): os.startfile(path)
            else: QMessageBox.critical(self, "Error", f"Cannot find File or Directory:\n\n{path}")

        buttonOpen = QPushButton()
        buttonOpen.setText("Open")
        buttonOpen.setFixedHeight(40)
        buttonOpen.clicked.connect(openFile)
        self.wListView.doubleClicked.connect(openFile)

        def openDirectory():
            file = self.getSelectedFile()
            if file is None: return
            
            path = file.directory if not file.isFolder else os.path.join(file.directory, file.fileName) 
            if os.path.exists(path): os.startfile(path)
            else: QMessageBox.critical(self, "Error", f"Cannot find File or Directory:\n\n{path}")

        buttonOpenPath = QPushButton()
        buttonOpenPath.setText("Open\nDirectory")
        buttonOpenPath.setFixedHeight(40)
        buttonOpenPath.clicked.connect(openDirectory)

        def showRateWindow():
            file = self.getSelectedFile()
            if file is None: return
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
            if file is None: return
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

        def onRenameButtonClick():
            file = self.getSelectedFile()
            if file is None: return
            text, ok = QInputDialog.getText(self, 'Rename', 'Enter new name..', text=file.name)
            if ok and len(text) > 0:
                DBInterface.instance().setFileName(file.index, text)
                self.loadFilesFromDB()

        buttonRen = QPushButton()
        buttonRen.setText("Rename")
        buttonRen.setFixedHeight(40)
        buttonRen.clicked.connect(onRenameButtonClick)


        def onRandomButtonClick():
            length = len(self.files)
            if length is 0 : return
            index = random.randrange(length)
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
            if file is None: return
            result = QMessageBox.question(self, "Confirm", f"Delete file from NSFW-Bolt?\nReal file is does not delete.\n\n{file.name}", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                DBInterface.instance().deleteFile(file.index)
                self.loadFilesFromDB()

        buttonDelete = QPushButton()
        buttonDelete.setText("Delete")
        buttonDelete.setFixedHeight(40)
        buttonDelete.clicked.connect(onDeleteButtonClick)

        def onRemoveButtonClick():
            file = self.getSelectedFile()
            if file is None: return
            result = QMessageBox.question(self, "Confirm", f"Delete file from NSFW-Bolt?\n\n{file.name}", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                path = self.getFilePath(file)
                print(path)
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                elif QMessageBox.warning(self, "Confirm", f"File or Folder does not exist.\nDo you want delete it from NSFW-Bolt?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes: return
                DBInterface.instance().deleteFile(file.index)
                self.loadFilesFromDB()

        buttonRemove = QPushButton()
        buttonRemove.setText("Delete\nFrom Disk")
        buttonRemove.setFixedHeight(40)
        buttonRemove.clicked.connect(onRemoveButtonClick)


        layout.addWidget(buttonOpen)
        layout.addWidget(buttonOpenPath)
        layout.addWidget(buttonRate)
        layout.addWidget(buttonTag)
        layout.addWidget(buttonRen)
        layout.addSpacing(20)
        layout.addWidget(buttonRandom)
        layout.addSpacing(20)
        layout.addWidget(buttonAdd)
        layout.addWidget(buttonDelete)
        layout.addWidget(buttonRemove)

        return layout

    def initUISearchBar(self):
        layout = QVBoxLayout()
        self.wSearchBar = QLineEdit()

        def searchTextChanged():
            self.loadFilesFromDB()
            
        self.wSearchBar.textChanged.connect(searchTextChanged)
        self.wSearchBar.setPlaceholderText("Enter ketword.. (Separate with commas(,). can use tag:[tag name], rate:[1~5], ext:[extension name]")

        layout1_1 = QHBoxLayout()
        layout1_1.setAlignment(Qt.AlignLeft)

        label = QLabel()
        label.setText("Search operator : ")

        self.wSearchOptionAnd = QRadioButton()
        self.wSearchOptionAnd.setText("AND")
        self.wSearchOptionAnd.setChecked(True)
        self.wSearchOptionAnd.clicked.connect(self.loadFilesFromDB)

        self.wSearchOptionOr = QRadioButton()
        self.wSearchOptionOr.setText("OR")
        self.wSearchOptionOr.clicked.connect(self.loadFilesFromDB)
        
        
        layout1_1.addWidget(label)
        layout1_1.addWidget(self.wSearchOptionAnd)
        layout1_1.addWidget(self.wSearchOptionOr)

        layout.addWidget(self.wSearchBar)
        layout.addLayout(layout1_1)
        return layout

    def inflateLayout(self):
        root = QHBoxLayout()

        layout1_1 = QVBoxLayout()
        layout1_1.addLayout(self.initUISearchBar())
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