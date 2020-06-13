import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from nFile import *

from TagListWindow import *

class TagWindow(QDialog):
    file = None
    listIdx = None

    wListView = None

    newTagId = None
    deletedTagIds = None

    def __init__(self, file, listIdx):
        super().__init__()
        self.file = file
        self.listIdx = listIdx
        self.newTagId = []
        self.deletedTagIds = []
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
        for tag in self.file.tags:
            model.appendRow(QStandardItem(tag))
        self.wListView.setModel(model)

    def initUI(self):
        self.setWindowTitle('Set Rate')
        self.setGeometry(100, 100, 200, 100)
        self.setPositionToCenterOfScreen()

        root = QVBoxLayout()
        root.addStretch(1)

        title = QLabel()
        title.setText(self.file.name)
        title.setFixedWidth(400)
        title.setWordWrap(True)
        titleFont = title.font()
        titleFont.setPointSize(12)
        title.setFont(titleFont)

        layout1 = QHBoxLayout()
        self.wListView = QListView()
        self.loadTagsIntoListView()

        layout1_1 = QVBoxLayout()

        def appendTag():
            win = TagListWindow()
            result = win.showModal()
            if result:
                tag = win.getResult()
                if any(tag.name in s for s in self.file.tags): return
                self.file.tags.append(tag.name)
                self.newTagId.append(tag.id)

        buttonNewTag = QPushButton("New")
        buttonNewTag.clicked.connect(appendTag)

        def removeTag():
            idx = self.getListIndex()
            if idx is None: return
            self.file.tags.pop(idx)
            self.loadTagsIntoListView()

        buttonDeleteTag = QPushButton("Delete")
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

        root.addWidget(title)
        root.addLayout(layout1)
        root.addLayout(layout2)
        root.addStretch(1)
        self.setLayout(root)

    def getResult(self):
        return self.newTagId, self.deletedTagIds

    def showModal(self):
        return super().exec_()