from PySide.QtCore import *
from PySide.QtGui import *

from entities import picpic_entities
from controlers import picpic_create_controlers
from controlers import picpic_shape_controlers


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
        if event.key() == Qt.Key_Return:
            if self.views()[0].active_tool == picpic_create_controlers.FREE:
                self.views()[0].free_shape.end_draw()
            self.views()[0].active_tool = None
            self.views()[0].window().create.uncheck_all()
            #HACK for update
            self.views()[0].free_shape.setPos(self.views()[0].free_shape.pos()+QPointF(0.1,0.1))
            self.views()[0].free_shape.update()

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

        self.active_tool = None
        self.click_pos = None
        self.release_pos = None

        self.free_shape = None
        self.free_core = None

    def mousePressEvent(self, event):
        self.click_pos = self.mapToScene(event.pos())
        if self.active_tool == picpic_create_controlers.FREE:
            if not self.free_node in self.scene.items():
                self.scene.add_picpicitem(self.free_node)
            if len(self.free_shape.core.vertex.value) == 0:
                self.free_shape.start_draw(self.click_pos)
            else:
                self.free_shape.add_line(self.click_pos)
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.release_pos = self.mapToScene(event.pos())
        length = QLineF(self.release_pos, self.click_pos).length()
        if len(self.scene.selectedItems()) == 0:
            if self.active_tool == picpic_create_controlers.CIRCLE and length > 25:
                circle_core = picpic_entities.PicPicShapeCore()
                circle_shape = picpic_shape_controlers.PicPicCircle(self.click_pos.toPoint(), self.release_pos.toPoint(), circle_core)
                circle_node = picpic_shape_controlers.PicPicNode(circle_shape)
                self.scene.add_picpicitem(circle_node)
            if self.active_tool == picpic_create_controlers.SQUARE and length > 25:
                square_core = picpic_entities.PicPicShapeCore()
                square_shape = picpic_shape_controlers.PicPicRect(self.click_pos.toPoint(), self.release_pos.toPoint(), square_core)
                square_node = picpic_shape_controlers.PicPicNode(square_shape)
                self.scene.add_picpicitem(square_node)
        QGraphicsView.mouseReleaseEvent(self, event)



class PicPicEmptyView(QWidget):
    def __init__(self):
        super(PicPicEmptyView, self).__init__()
        lay = QVBoxLayout(self)
        self.but = QPushButton("First, add a background")
        self.but.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lay.addWidget(self.but)
        self.adjustSize()

        self.but.clicked.connect(self.add_background)

    def add_background(self):
        tab = self.window().tab
        tab.add_tab_background(window=self.window())
