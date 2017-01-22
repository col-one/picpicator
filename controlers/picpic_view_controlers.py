from PySide.QtCore import *
from PySide.QtGui import *

class PicPicScene(QGraphicsScene):
    def __init__(self):
        super(PicPicScene, self).__init__()
        self.setSceneRect(-50000, -50000, 100000, 100000)
        self.background =  QGraphicsPixmapItem()
        self.items_ = []

    def add_background(self, img):
        pix = QPixmap(img)
        self.background.setPixmap(pix)
        self.background.setZValue(-1000)
        self.background.setOffset(-0.5 * QPointF(pix.width(), pix.height()))
        self.addItem(self.background)
        self.views()[0].setMaximumHeight(pix.height())
        self.views()[0].setMinimumHeight(pix.height())
        self.views()[0].setMaximumWidth(pix.width())
        self.views()[0].setMinimumWidth(pix.width())

    def add_picpicitem(self, item):
        self.addItem(item)
        self.items_.append(item)
        item.item.core.name.value += str(len(self.items_))







