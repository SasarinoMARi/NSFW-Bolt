import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from nFile import *

class RateWindow(QDialog):
    file = None
    wStars = []
    currentRate = None

    def __init__(self, file):
        super().__init__()
        self.file = file
        self.currentRate = file.rate if not file.rate is None else 0
        self.wStars = []
        self.initUI()

    def setPositionToCenterOfScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def findStarRate(self, object):
        for i in range(len(self.wStars)):
            if self.wStars[i] is object:
                return i+1
        return None

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress:
            x = self.findStarRate(object)
            self.currentRate = x
            for i in range(x):
                self.wStars[i].setIcon(QIcon(QPixmap("images/star-filled.png")))
            for i in range(x, len(self.wStars)):
                self.wStars[i].setIcon(QIcon(QPixmap("images/star.png")))
            return True
        elif event.type() == QEvent.HoverMove:
            x = self.findStarRate(object)
            if x is None: return False
            if x < self.currentRate: return True
            for i in range(self.currentRate, x):
                self.wStars[i].setIcon(QIcon(QPixmap("images/star-highlighted.png")))
            for i in range(x, len(self.wStars)):
                self.wStars[i].setIcon(QIcon(QPixmap("images/star.png")))
            return True
        return False

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

        layout1_1 = QHBoxLayout()
        stars = []
        for i in range(5):
            star = QPushButton()
            pixmap = QPixmap("images/star-filled.png" if i < self.currentRate else "images/star.png")
            star.setIcon(QIcon(pixmap))
            star.setIconSize(pixmap.rect().size())
            star.setFixedSize(pixmap.rect().size())
            star.setStyleSheet("border: none;")
            star.installEventFilter(self)
            self.wStars.append(star)
            layout1_1.addWidget(star)

        layout1_2 = QHBoxLayout()
        btnOK = QPushButton("Confirm")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        
        layout1_2.addWidget(btnOK)
        layout1_2.addWidget(btnCancel)

        root.addWidget(title)
        root.addLayout(layout1_1)
        root.addLayout(layout1_2)
        root.addStretch(1)
        self.setLayout(root)

    def onOKButtonClicked(self):
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()