import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from nFile import *

class AddFileWindow(QDialog):
    results = None
    wListView = None

    def __init__(self):
        super().__init__()
        self.results = []
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

    def loadListView(self):
        model = QStandardItemModel()
        for path in self.results:
            model.appendRow(QStandardItem(path))
        self.wListView.setModel(model)

    def initUI(self):
        self.setWindowTitle('Add Files')
        self.setGeometry(100, 100, 600, 400)
        self.setPositionToCenterOfScreen()

        root = QHBoxLayout()

        self.wListView = QListView()
        self.loadListView()

        def addFiles():
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.ExistingFiles)
            result = dialog.exec()
            if result:
                self.results.extend(dialog.selectedFiles())
                self.loadListView()
        
        def addFolder(): 
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.DirectoryOnly)
            result = dialog.exec()
            if result:
                self.results.extend(dialog.selectedFiles())
                self.loadListView()
        
        def deletePath():
            idx = self.getListIndex()
            if idx is None: return
            self.results.pop(idx)
            self.loadListView()

        layout1_1 = QVBoxLayout()
        btnAddFile = QPushButton("Add Files")
        btnAddFile.clicked.connect(addFiles)
        btnAddFolder = QPushButton("Add Folder")
        btnAddFolder.clicked.connect(addFolder)
        btnDelete = QPushButton("Delete")
        btnDelete.clicked.connect(deletePath)
        btnOK = QPushButton("Confirm")
        btnOK.clicked.connect(lambda: self.accept())
        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(lambda: self.reject())
        
        layout1_1.addWidget(btnAddFile)
        layout1_1.addWidget(btnAddFolder)
        layout1_1.addWidget(btnDelete)
        layout1_1.addStretch(1)
        layout1_1.addWidget(btnOK)
        layout1_1.addWidget(btnCancel)

        root.addWidget(self.wListView)
        root.addLayout(layout1_1)
        self.setLayout(root)

    def getResult(self):
        return self.results

    def showModal(self):
        return super().exec_()