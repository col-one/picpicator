from PySide.QtCore import *
from PySide.QtGui import *

class PicPicScene(QGraphicsScene):
    def __init__(self, editor=None):
        super(PicPicScene, self).__init__()
        self.setSceneRect(-50000, -50000, 100000, 100000)
        self.background =  QGraphicsPixmapItem()
        self.items_ = []
        self.editor = editor

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
        self.setSceneRect(self.itemsBoundingRect())


    def add_picpicitem(self, item):
        self.addItem(item)
        self.items_.append(item)
        item.item.core.name.value += str(len(self.items_))
        item.item.signal.fired.connect(self.pop)

    @Slot(list)
    def pop(self, event):
        self.editor.populate_attr(event)

    def mousePressEvent(self, event):
        self.editor.delete_attr_panel()
        QGraphicsScene.mousePressEvent(self, event)

    def keyPressEvent(self, event):
        super(PicPicScene, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            items = self.selectedItems()
            for item in items:
                self.removeItem(item)
                del item
            self.editor.delete_attr_panel()

class PicPicView(QGraphicsView):
    def __init__(self, scene=None):
        super(PicPicView, self).__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setBackgroundBrush(QColor(70, 70, 70))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = scene

        self.setScene(self.scene)

class PicPicEmptyView(QWidget):
    def __init__(self):
        super(PicPicEmptyView, self).__init__()
        lay = QVBoxLayout(self)
        self.but = QPushButton("First add a background")
        self.but.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lay.addWidget(self.but)
        self.adjustSize()

        self.but.clicked.connect(self.add_background)

    def add_background(self):
        tab = self.parent().parent()
        id = tab.currentIndex()
        dialog = QFileDialog()
        dialog.setNameFilter("Images (*.png *.tiff *.tga *.jpg)")
        dialog.setViewMode(QFileDialog.Detail)
        fileName = QFileDialog.getOpenFileName(self, "Open File", "Images (*.png *.tga *.tiff *.jpg)")
        if fileName[0] != '':
            print fileName
            tab.removeTab(id)
            self.scene_ = PicPicScene()
            self.view = PicPicView(scene=self.scene_)
            self.scene_.editor = self.window().editor
            self.scene_.add_background(fileName[0])
            tab.addTab(self.view, "new tab (click to rename)")
            tab.setCurrentIndex(id)

