import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from DBInterface import *
from nFile import *

class TagListWindow(QDialog):
    tags = None
    wListView = None

    def __init__(self):
        super().__init__()
        self.tags = DBInterface.instance().getTags()
        self.initUI()

    def setPositionToCenterOfScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def getListIndex(self):
        idxes = self.wListView.selectedIndexes()
        if len(idxes) == 0: return None
        return idxes[0].row()
    
    def loadTagsIntoListView(self):
        model = QStandardItemModel()
        for tag in self.tags:
            model.appendRow(QStandardItem(tag.name))
        self.wListView.setModel(model)

    def initUI(self):
        self.setWindowTitle('Edit Tag')
        self.setGeometry(100, 100, 200, 200)
        self.setPositionToCenterOfScreen()

        root = QVBoxLayout()
        root.addStretch(1)

        layout1 = QHBoxLayout()
        self.wListView = QListView()
        self.loadTagsIntoListView()

        layout1_1 = QVBoxLayout()
        layout1_1.setAlignment(Qt.AlignTop)

        def appendTag():
            win = SimpleInputWindow("Enter new tag")
            result = win.showModal()
            if result:
                name = win.getResult()
                DBInterface.instance().addTag(name)
                self.tags = DBInterface.instance().getTags()
                self.loadTagsIntoListView()

        buttonNewTag = QPushButton("New Tag")
        buttonNewTag.clicked.connect(appendTag)

        def removeTag():
            idx = self.getListIndex()
            if idx is None: return
            self.tags.pop(idx)
            self.loadTagsIntoListView()

        buttonDeleteTag = QPushButton("Delete Tag")
        buttonDeleteTag.clicked.connect(removeTag)

        layout1_1.addWidget(buttonNewTag)
        layout1_1.addWidget(buttonDeleteTag)

        layout1.addWidget(self.wListView)
        layout1.addLayout(layout1_1)

        layout2 = QHBoxLayout()
        btnOK = QPushButton("Confirm")
        btnOK.clicked.connect(lambda: self.accept())
        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(lambda: self.reject())
        
        layout2.addWidget(btnOK)
        layout2.addWidget(btnCancel)

        root.addLayout(layout1)
        root.addLayout(layout2)
        root.addStretch(1)
        self.setLayout(root)

    def showModal(self):
        return super().exec_()

    def getResult(self):
        idx = self.getListIndex()
        if idx is None: return None
        return self.tags[idx]


class SimpleInputWindow(QDialog):
    Result = None

    def __init__(self, title):
        super().__init__()
        self.title = title
        self.initUI()

    def setPositionToCenterOfScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 200, 100)
        self.setPositionToCenterOfScreen()

        root = QVBoxLayout()
        root.addStretch(1)

        self.Result = QLineEdit()

        layout1 = QHBoxLayout()
        btnOK = QPushButton("Confirm")
        btnOK.clicked.connect(lambda: self.accept())
        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(lambda: self.reject())
        
        layout1.addWidget(btnOK)
        layout1.addWidget(btnCancel)

        root.addWidget(self.Result)
        root.addStretch(1)
        root.addLayout(layout1)
        root.addStretch(1)
        self.setLayout(root)

    def showModal(self):
        return super().exec_()

    def getResult(self):
        return self.Result.text()