from PySide.QtCore import *
from PySide.QtGui import *

from picpic_properties_controlers import *
from entities.picpic_entities import *

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(1)
        self.setContentsMargins(0,0,0,0)


class PicPicFrame(QWidget):
    def __init__(self):
        super(PicPicFrame, self).__init__()
        self.lay = QVBoxLayout(self)
        self.lay.setAlignment(Qt.AlignTop)
        self.setFixedWidth(200)
        self.sep = QHLine()

        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0,0,0,0)

    def populate_attr(self, attr_widgets):
        self.delete_attr_panel()
        for widget in attr_widgets:
            self.lay.addWidget(widget)
            self.sep = QHLine()
            self.lay.addWidget(self.sep)

    def delete_attr_panel(self):
        for i in reversed(range(self.lay.count())):
            wi = self.lay.itemAt(i).widget()
            self.lay.removeWidget(wi)
            wi.setParent(None)
            del wi

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(120,120,120,255))
        rect = self.rect()
        rect.adjust(0,0,-1,-1)
        painter.drawRect(rect)
        painter.end()

def PicPicAttrGen(core):
    all_attr = core.__dict__
    widgets_attr = []
    for label in all_attr:
        if all_attr[label] is None or not all_attr[label].expo :
            continue
        _type = all_attr[label].type
        if _type == STRING:
            widget = PicPicString(all_attr[label], label)
        elif _type == FLOAT:
            widget = PicPicFloat(all_attr[label], label)
        elif _type == COLOR:
            widget = PicPicColor(all_attr[label], label)
        else:
            widget = QWidget()
        widgets_attr.append(widget)
        widgets_attr = sorted(widgets_attr, key=lambda x: x.expo_order)
    return widgets_attr
