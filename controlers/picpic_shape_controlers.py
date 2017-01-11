from PySide.QtGui import *
from PySide.QtCore import *
from picpic_entities import *

class PicPicShape(QGraphicsItem):
    def __init__(self, core=PicPicFreeCore):
        super(PicPicShape, self).__init__()
        #all flags
        self.setFlags(
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        #attributes
        self.core=core
        self.cc_over_color = QColor(255, 255, 255, 150)
        self.cc_select_color = QColor(255, 255, 255, 100)
        self.core.pen_color = QColor(0,0,0,0)
        self.core.pen_width = 4
        self.core.over_color = QColor(255, 255, 255, 255)
        self.bb_rect = QRect()
        self.hovered = False
        self.pen = QPen()
        self.cc_hover_pen = QPen()
        self.cc_hover_pen_width = 2


        #override
        self.pen.setColor(self.core.pen_color)
        self.pen.setWidth(self.core.pen_width)
        #graphicsitems attributes
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return self.bb_rect

    def paint(self, painter, option, widget):
        self.cc_hover_pen.setWidth(self.cc_hover_pen_width)
        if self.hovered:
            self.cc_hover_pen.setColor(self.cc_over_color)
        elif self.isSelected():
            self.cc_hover_pen.setColor(self.cc_select_color)
        else:
            self.cc_hover_pen.setColor(self.core.pen_color)
        painter.setPen(self.cc_hover_pen)
        painter.drawRect(self.bb_rect)
        self.scene().update()

    def hoverEnterEvent(self, event):
        self.hovered = True

    def hoverLeaveEvent(self, event):
        self.hovered = False



class PicPicCircle(PicPicShape):
    def __init__(self, center, radius, core):
        super(PicPicCircle, self).__init__(core=core)

        self.center = center
        self.radius = radius
        self.circle_rect = QRect(center.x()-radius, center.y()-radius, radius*2+center.x(), radius*2+center.y())
        self.bb_rect = self.circle_rect
        self.core.color = QColor(0,0,0,255)

    def paint(self, painter, option, widget):
        super(PicPicCircle, self).paint(painter, option, widget)
        painter.setPen(self.core.pen_color)
        painter.setBrush(self.core.color)
        painter.drawEllipse(self.center, self.radius, self.radius)


class PicPicRect(PicPicShape):
    def __init__(self, bottom, top, core):
        super(PicPicRect, self).__init__(core=core)

        self.bottom = bottom
        self.top = top
        self.rect = QRect(bottom, top)
        self.bb_rect = self.rect
        self.core.color = QColor(0,0,0,255)

    def paint(self, painter, option, widget):
        super(PicPicRect, self).paint(painter, option, widget)
        painter.setBrush(self.core.color)
        painter.drawRect(self.rect)

class PicPicFreeDraw(PicPicShape):
    def __init__(self, core):
        super(PicPicFreeDraw, self).__init__(core=core)
        if not type(core) == PicPicFreeCore:
            raise TypeError("core must be type PicPicFree")
        self.core.path = QPainterPath()
        self.core.color = QColor(255,255,0)

    def start_draw(self, point):
        self.core.vertex.append(point)
        self.core.path.moveTo(point)

    def add_line(self, point):
        self.core.vertex.append(point)
        self.core.path.lineTo(point)

    def end_draw(self):
        self.core.vertex.append(self.core.path.pointAtPercent(0.0))
        self.core.path.closeSubpath()
        self.bb_rect = self.mapRectToScene(self.core.path.controlPointRect())

    def paint(self, painter, option, widget):
        super(PicPicFreeDraw, self).paint(painter, option, widget)
        painter.setPen(Qt.NoPen)
        if self.hovered:
            painter.setBrush(self.core.over_color)
        else:
            painter.setBrush(self.core.color)
        painter.drawPath(self.core.path)