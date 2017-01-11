import copy
from PySide.QtGui import *
from PySide.QtCore import *

import picpic_entities
import picpic_controlers

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.view = View(self)
        self.button = QPushButton('Add Shape', self)
        self.buttonc = QPushButton('Color', self)
        self.opacity = QSlider(Qt.Horizontal)

        widget_right = QWidget(self)
        lay_right = QVBoxLayout(widget_right)
        lay_right.addWidget(self.button)
        lay_right.addWidget(self.buttonc)
        lay_right.addWidget(self.opacity)

        self.opacity.setMinimum(0)
        self.opacity.setMaximum(255)

        layout = QHBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(widget_right)

        self.button.clicked.connect(self.handleClearView)
        self.buttonc.clicked.connect(self.change_color)
        self.opacity.valueChanged.connect(self.change_opacity)

    def handleClearView(self):
        shape_core = picpic_entities.PicPicFree()
        shape = picpic_controlers.PicPicFreeDraw(core=shape_core)
        shape.setZValue(1000)
        self.view.shape.append(shape)
        self.view.id += 1
        self.view.scene().addItem(self.view.shape[self.view.id])
        shape.setParentItem(self.view.bck)
        self.view.start_draw = True

    def change_color(self):
        self.view.scene().selectedItems()[0].color = QColor(255, 255, 255)

    def change_opacity(self):
        #for item in self.view.scene().selectedItems():
        #    print item.color
        #n_color = self.view.scene().selectedItems()[0].color
        new_color = self.view.scene().selectedItems()[0].color
        new_color.setAlpha(255-self.opacity.value())
        self.view.scene().selectedItems()[0].color = new_color
        #self.view.scene().selectedItems()[0].color = new_color

class View(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.setRenderHint(QPainter.Antialiasing)
        # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setBackgroundBrush(QColor(70, 70, 70))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.bck = QGraphicsPixmapItem()
        self.img = QPixmap("./Jadina_Fond.jpg")
        self.bck.setPixmap(self.img)
        self.bck.setZValue(-1000)
        self.bck.setOffset( -0.5 * QPointF( self.img.width(), self.img.height() ) )

        self.circle = picpic_controlers.PicPicRect(QPoint(0,0), QPoint(100,100), core=picpic_entities.PicPicShape)

        self.start_draw = False
        self.shape = []
        self.id = -1

        self.setMaximumHeight(self.img.height())
        self.setMinimumHeight(self.img.height())
        self.setMaximumWidth(self.img.width())
        self.setMinimumWidth(self.img.width())

        self.scene_ = QGraphicsScene()
        self.scene_.setSceneRect(-50000, -50000, 100000, 100000)
        self.setScene(self.scene_)
        self.scene_.addItem(self.bck)
        self.scene_.addItem(self.circle)


    def mousePressEvent(self, event):
        if not self.start_draw:
            return QGraphicsView.mousePressEvent(self, event)
        if len(self.shape[self.id].core.vertex) == 0:
            self.shape[self.id].start_draw(self.mapToScene(event.pos()))
            #self.shape[self.id].set_bounding(self.mapToScene(event.pos()))
        else:
            self.shape[self.id].add_line(self.mapToScene(event.pos()))
        QGraphicsView.mousePressEvent(self, event)

    def keyPressEvent(self, event):
        super(View, self).keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.shape[self.id].end_draw()
            self.start_draw = False
            print self.shape[self.id].vertex

class Shape(QGraphicsItem):
    def __init__(self):
        super(Shape, self).__init__()
        self.setFlags(
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )

        self.setAcceptHoverEvents(True)
        self.setSelected(True)

        self.rect = QRect()
        self.first_point = True
        self.path_draw = QPainterPath()
        self.color = QColor(0.0, 220.0, 0.0)
        self.light_color = self.color.lighter(150)
        self.begin_point = None
        self.vertex = []
        self.closed = False
        self.over = False
        self.rect = QRect(0,0,50,50)
        self.over_color = QColor(255, 255, 255, 150)
        self.select_color = QColor(255, 255, 255, 100)

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def set_bounding(self, click):
        click = self.mapToScene(click)
        #self.rect = QRect(click.x(), click.y(), 50, 50)

    def start_point(self, point):
        self.begin_point = point
        self.path_draw.moveTo(point)
        self.first_point = False
        self.vertex.append(point)

    def add_point(self, point):
        self.path_draw.lineTo(point)
        self.vertex.append(point)

    def close_path(self):
        self.path_draw.closeSubpath()
        self.closed = True
        self.setSelected(True)
        self.setActive(True)
        self.rect = self.mapRectToScene(self.path_draw.controlPointRect())

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        if self.over:
            painter.setPen(self.over_color)
            painter.drawRect(self.rect)
        elif self.isSelected():
            painter.setPen(self.select_color)
            painter.drawRect(self.rect)
            #
            # painter.setBrush(self.light_color)
            # painter.setBrush(self.light_color)
        painter.setPen(self.color)
        painter.setBrush(self.color)
        painter.drawPath(self.path_draw)
        painter.setPen(QColor(255,0,0))
        painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.path_draw.controlPointRect())
        self.scene().update()

    def hoverEnterEvent(self, event):
        self.over = True
        self.scene().update()
    def hoverLeaveEvent(self, event):
        self.over = False
        self.scene().update()


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
sys.exit(app.exec_())