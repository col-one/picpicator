from PySide.QtCore import *
from PySide.QtGui import *

from picpic_properties_controlers import *
from entities.picpic_entities import *

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        # self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(10)
        self.setContentsMargins(0,0,0,0)


class PicPicFrame(QWidget):
    def __init__(self):
        super(PicPicFrame, self).__init__()
        self.lay = QVBoxLayout(self)
        self.lay.setAlignment(Qt.AlignTop)
        self.setFixedWidth(200)

        self.sep = QHLine()

        self.list = QListWidget()
        #self.list.setStyleSheet("background-color: #455122")
        self.list.setSpacing(0)
        self.list.setContentsMargins(0,0,0,0)

        self.lay.addWidget(self.sep)
        self.lay.addWidget(self.list)

        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0,0,0,0)

    def populate_attr(self, attr_widgets):
        self.list.clear()
        for widget in attr_widgets:
            item = QListWidgetItem()
            item.setSizeHint(QSize(180, 65))
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

def PicPicAttrGen(core):
    all_attr = core.__dict__
    widgets_attr = []
    for label in all_attr:
        if all_attr[label] is None:
            continue
        _type = all_attr[label].type
        if _type == STRING:
            widget = PicPicString(all_attr[label], label)
        elif _type == FLOAT:
            widget = PicPicFloat(all_attr[label], label)
        elif _type == COLOR:
            widget = PicPicColor(all_attr[label], label)
        else:
            widget = None
        widgets_attr.append(widget)
    return widgets_attr
