from nTag import *

class nFile:
    index = None            # DB 내부 인덱스
    name = None             # 사용자 지정 이름
    fileName = None         # 실제 파일명
    directory = None        # 소속 디렉토리
    isFolder = None         # 폴더인지 여부
    extension = None        # 확장자
    thumbnail = None        # 섬네일
    rate = None             # 별점
    tags = None             # 태그
    serialNumber = None     # 품번
    hash = None             # 해시

    @staticmethod 
    def createWithRow(row):
        instance = nFile()
        instance.index = row['idx']
        instance.name = row['name']
        instance.fileName = row['filename']
        instance.directory = row['directory']
        instance.isFolder = row['isFolder']
        instance.extension = row['extension']
        instance.thumbnail = row['thumbnail']
        instance.rate = row['rate']
        instance.serialNumber = row['serialNumber']
        instance.hash = row['hash']

        tagNames = str(row['tagNames']).split(',') if not row['tagNames'] is None else []
        tagIndexes = str(row['tagIds']).split(',') if not row['tagIds'] is None else []
        if len(tagNames) != len(tagIndexes):
            print(f"[{row['idx']}] : Tag names and indexes is not matched.")
            print(f"\tTag names : {row['tagNames']}")
            print(f"\tTag indexes : {row['tagIds']}")
            return None
        instance.tags = []
        for i in range(len(tagNames)):
            instance.tags.append(nTag(tagIndexes[i], tagNames[i]))
        return instance

    def __str__(self):
        return f"[{self.index}] {self.name}\n\t{self.directory}/{self.fileName} (ext: {self.extension})\n\tHash: {self.hash}"

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FileModel(QAbstractListModel):
    files = None

    def __init__(self, parent=None, files=[]):
        QAbstractListModel.__init__(self, parent)
        self.files = files

    def rowCount(self, parent=QModelIndex()):
        return len(self.files)

    # def index(self, row, column, index):
    #     return self.createIndex(row, column, None)


    def data(self, index, role):
        if index.isValid() and role==Qt.DisplayRole: 
            return QVariant(self.files[index.row()].name)
        else:
            return QVariant()

    # def setData(self, index, value, role):
    #     print("setD")
    #     if index.isValid: 
    #         self.files.append(value)
    #         self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
    #         return True
    #     return False

    # @pyqtSlot(nFile)
    # def append(self, file):
    #     print("apd")
    #     self.beginInsertRows(QModelIndex(), self.rowCount(None), self.rowCount(None))
    #     self.files.append(file)
    #     self.endInsertRows()
class FileModelDelegate(QStyledItemDelegate):
    margins = QMargins(0, 0, 0, 0)
    spacingHorizontal = 0
    spacingVertical = 0

    def __init__(self, parent):
        super(FileModelDelegate, self).__init__(parent)

    def timestampFontPointSize(self, font):
	    return 0.85*font.pointSize()

    def timestampBox(self, opt, index):
	    font = QFont(opt.font)

	    font.setPointSizeF(self.timestampFontPointSize(opt.font))

	    return QFontMetrics(font).boundingRect(str(index.data(Qt.UserRole))).adjusted(0, 0, 1, 1)

    def messageBox(self, opt):
	    font = QFont(opt.font)

	    return QFontMetrics(font).boundingRect(opt.text).adjusted(0, 0, 1, 1)

    def paint(self, painter, option, index):
        file = index.data()
        if not isinstance(file, nFile): 
            QStyledItemDelegate.paint(self, painter, option, index)
            return


        # print(f"file:{file.name}")
        opt = QStyleOptionViewItem(option)
        super(FileModelDelegate, self).initStyleOption(option, index)

        palette = QPalette(opt.palette)
        rect = QRect(opt.rect)
        contentRect = QRect(rect.adjusted(self.margins.left(), self.margins.top(), self.margins.right(), self.margins.bottom()));

        if index.model().rowCount() -1 == index.row(): lastIndex = True
        else: lastIndex = False
        bottomEdge = rect.bottom()

        font = QFont(opt.font)
        font.setPointSize(self.timestampFontPointSize(opt.font))

        painter.save()
        painter.setClipping(True)
        painter.setClipRect(rect)
        painter.setFont(opt.font)

        # Draw background
        painter.fillRect(rect, palette.highlight().color() if (opt.state & QStyle.State_Selected) else palette.light().color())

        # Draw bottom line
        painter.setPen(palette.dark().color() if lastIndex else palette.mid().color())
        painter.drawLine(rect.left() if lastIndex else self.margins.left(), bottomEdge, rect.right(), bottomEdge)

        # Draw message icon
        # if (hasIcon)
        #     painter->drawPixmap(contentRect.left(), contentRect.top(),
        #                         opt.icon.pixmap(m_ptr->iconSize));

        # Draw timestamp
        timeStampRect = QRect(self.timestampBox(opt, index))

        timeStampRect.moveTo(self.margins.left() + self.spacingHorizontal, contentRect.top()) 

        painter.setFont(font)
        painter.setPen(palette.text().color())
        painter.drawText(timeStampRect, Qt.TextSingleLine, f'Tag : {", ".join(file.tags)}')

        # Draw message text
        messageRect = QRect(self.messageBox(opt))
        print(f"rw : {messageRect.width()}, rh : {messageRect.height()}")

        messageRect.moveTo(timeStampRect.left(), timeStampRect.bottom() + self.spacingVertical)

        painter.setFont(opt.font)
        painter.setPen(palette.windowText().color())
        painter.drawText(messageRect, Qt.TextSingleLine, file.name)

        painter.restore()

    def sizeHint(self, option, index):
        file = index.data()
        if not isinstance(file, nFile): return QStyledItemDelegate.sizeHint(self, option, index)
        # return super().sizeHint(self, option, index)
        opt = QStyleOptionViewItem(option)
        super(FileModelDelegate, self).initStyleOption(option, index)

        textHeight = self.timestampBox(opt, index).height() + self.spacingVertical +self.messageBox(opt).height()
        h = textHeight
        print (f"tb:{self.timestampBox(opt, index).height()}, tb:{self.messageBox(opt).height()}")

        return QSize(opt.rect.width(), self.margins.top() + h + self.margins.bottom())

class _FileView(QWidget):
    defaultThumbnail = "thumb/sample.jpg"

    thumbnail = None
    name = None
    tags = None
    rate = None
    index = -1

    def __init__(self, root, file):
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
        self.name.setFixedWidth(540)
        self.name.setFixedHeight(60)
        # self.name.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.name.setWordWrap(True)
        f = self.name.font()
        f.setFamily('맑은 고딕')
        f.setPointSize(12)
        f.bold()
        self.name.setFont(f)
        rightside.addWidget(self.name)

        rightside.addStretch(1)
        
        self.rate = QLabel(root)
        self.rate.setFixedWidth(540)
        f = self.rate.font()
        f.setFamily('맑은 고딕')
        f.setPointSize(10)
        self.rate.setFont(f)
        rightside.addWidget(self.rate)
        

        self.tags = QLabel(root)
        self.tags.setFixedWidth(540)
        f = self.tags.font()
        f.setFamily('맑은 고딕')
        f.setPointSize(10)
        self.tags.setFont(f)
        rightside.addWidget(self.tags)

        rightside.setContentsMargins(10, 0, 0, 0)     
        content.addLayout(rightside)
        content.setSpacing(0)
        layout.addLayout(content, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.resize(100, 120)
        self.setLayout(layout)

        
        self.setIndex(file.index)
        self.setName(file.name)
        self.setRate(file.rate)
        self.setTags(file.tags)
        # self.setMinimumSize(100, 100)

    def setIndex(self, index):
        self.index = index

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