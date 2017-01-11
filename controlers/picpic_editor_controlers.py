from PySide.QtCore import *
from PySide.QtGui import *

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(20)


class PicPicFrame(QWidget):
    def __init__(self):
        super(PicPicFrame, self).__init__()
        self.lay = QVBoxLayout(self)
        self.lay.setAlignment(Qt.AlignTop)
        self.sep = QHLine()

        self.list = QListWidget()

        self.lay.addWidget(self.sep)
        self.lay.addWidget(self.list)

