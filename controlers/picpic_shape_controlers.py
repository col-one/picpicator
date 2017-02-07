from PySide.QtCore import *
from PySide.QtGui import *
import copy

from entities.picpic_entities import *
from controlers.picpic_editor_controlers import *

class PicSignal(QObject):
    fired = Signal(list)
    deleted = Signal(list)


class PicPicNode(QGraphicsItem):
    def __init__(self, item):
        super(PicPicNode, self).__init__()
        #all flags
        self.setFlags(
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.color = QColor(250,250,250,255)
        self.item = item
        self.item.setParentItem(self)

        self.scale_attr = None
        self.mtr = QTransform()

    @Slot(float)
    def scale_item(self, sx):
        self.item.core.scale.value = sx
        self.mtr = QTransform.fromScale(self.item.core.scale.value, self.item.core.scale.value)
        self.mtr.rotate(self.item.core.rotate.value, Qt.ZAxis)
        self.setTransform(self.mtr)

    @Slot(float)
    def rotate_item(self, sx):
        self.item.core.rotate.value = sx
        self.mtr = QTransform.fromScale(self.item.core.scale.value, self.item.core.scale.value)
        self.mtr.rotate(self.item.core.rotate.value, Qt.ZAxis)
        self.setTransform(self.mtr)

    def mousePressEvent(self, event):
        for widget in self.item.attr_widgets:
            if widget.label_name == "scale":
                self.scale_attr = widget
                self.scale_attr.signal.changed.connect(self.scale_item)
            if widget.label_name == "rotate":
                self.scale_attr = widget
                self.scale_attr.signal.changed.connect(self.rotate_item)
        QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.item.switch_color(event)
        QGraphicsItem.mouseReleaseEvent(self, event)

    def boundingRect(self, *args, **kwargs):
        self.rect = copy.deepcopy(self.item.boundingRect())
        self.rect = self.rect.adjusted(-5,-5,5,5)
        return self.rect

    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setBrush(Qt.NoBrush)
            painter.setPen(self.color)
            painter.drawRect(self.rect)

class PicPicShape(QGraphicsItem):
    def __init__(self, core=PicPicFreeCore):
        super(PicPicShape, self).__init__()
        self.signal = PicSignal()
        #attributes
        self.core=core
        self.cc_over_color = QColor(255, 255, 255, 150)
        self.cc_select_color = QColor(255, 255, 255, 100)
        try:
            self.core.pen_color.value = QColor(*self.core.pen_color.value)
        except TypeError:
            pass
        try:
            self.core.color.value = QColor(*self.core.color.value)
        except TypeError:
            pass
        try:
            self.core.click_color.value = QColor(*self.core.click_color.value)
        except TypeError:
            pass

        self.core.pen_width.value = self.core.pen_width.value
        self.core.over_color.value = self.core.color.value.lighter(150)

        self.bb_rect = QRect()
        self.hovered = False
        self.pen = QPen()
        self.brush = QColor()
        self.cc_hover_pen = QPen()
        self.cc_hover_pen_width = 2
        self.cc_click_action = (PicPicAttrGen, self.core)
        self.attr_widgets = []

        #override
        self.pen.setColor(self.core.pen_color.value)
        self.pen.setWidth(self.core.pen_width.value)
        self.brush = self.core.color.value
        #graphicsitems attributes
        self.setAcceptHoverEvents(True)

    def change_color(self, brush, pen):
        self.core.color.value = brush
        self.core.pen_color.value = pen
        self.pen.setColor(self.core.pen_color.value)
        self.pen.setWidth(self.core.pen_width.value)
        self.brush = self.core.color.value

    def boundingRect(self):
        return self.bb_rect

    def paint(self, painter, option, widget):
        self.core.color.value.setAlpha(self.core.opacity.value / 100 * 255)
        self.core.over_color.value.setAlpha(self.core.opacity.value / 100 * 255)
        self.core.click_color.value.setAlpha(self.core.opacity.value / 100 * 255)
        painter.setBrush(self.brush)
        self.pen.setWidth(self.core.pen_width.value)
        painter.setPen(self.pen)
        self.scene().update()

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.brush = self.core.over_color.value

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.brush = self.core.color.value

    def mousePressEvent(self, event):
        ret = self.cc_click_action[0](self.cc_click_action[1])
        self.attr_widgets = ret
        self.signal.fired.emit(self.attr_widgets)
        self.brush = self.core.click_color.value
        QGraphicsItem.mousePressEvent(self, event)

    def switch_color(self, event):
        self.brush = self.core.color.value


class PicPicCircle(PicPicShape):
    def __init__(self, center, radius, core):
        super(PicPicCircle, self).__init__(core=core)

        self.center = center
        self.radius = radius
        self.circle_rect = QRect(center, radius)
        self.bb_rect = self.circle_rect

    def paint(self, painter, option, widget):
        super(PicPicCircle, self).paint(painter, option, widget)
        painter.drawEllipse(self.circle_rect)

class PicPicRect(PicPicShape):
    def __init__(self, bottom, top, core):
        super(PicPicRect, self).__init__(core=core)
        self.bottom = bottom
        self.top = top
        self.rect = QRect(self.bottom, self.top)
        self.bb_rect = self.rect

    def paint(self, painter, option, widget):
        super(PicPicRect, self).paint(painter, option, widget)
        painter.drawRect(self.rect)

class PicPicFreeDraw(PicPicShape):
    def __init__(self, core):
        super(PicPicFreeDraw, self).__init__(core=core)
        if not type(core) == PicPicFreeCore:
            raise TypeError("core must be type PicPicFree")
        self.path = QPainterPath()

    def start_draw(self, point):
        self.core.vertex.value = point
        self.path.moveTo(point)

    def add_line(self, point):
        self.core.vertex.value = point
        self.path.lineTo(point)

    def end_draw(self):
        self.core.vertex.value = self.path.pointAtPercent(0.0)
        self.path.closeSubpath()

    def boundingRect(self):
        return self.path.controlPointRect()

    def paint(self, painter, option, widget):
        super(PicPicFreeDraw, self).paint(painter, option, widget)
        painter.drawPath(self.path)

class PicPicText(PicPicShape):
    def __init__(self, bottom, top, core):
        super(PicPicText, self).__init__(core=core)
        self.bottom = bottom
        self.top = top
        self.rect = QRect(self.bottom, self.top)
        self.bb_rect = self.rect

    def paint(self, painter, option, widget):
        super(PicPicText, self).paint(painter, option, widget)
        self.font = painter.font()
        self.font.setPointSize(self.font.pointSize() * self.core.size.value)
        painter.setFont(self.font)
        painter.drawText(self.rect, self.core.text.value)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.pen = QPen(self.core.over_color.value)

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.pen = QPen(self.core.color.value)

    def mousePressEvent(self, event):
        super(PicPicText, self).mousePressEvent(event)
        self.pen = QPen(self.core.click_color.value)

class PicPicButton(QPushButton):
    def __init__(self, bottom, top, core):
        super(PicPicButton, self).__init__()
        self.signal = PicSignal()
        self.core = core
        self.bottom = bottom
        self.top = top
        self.setText(self.core.name.value)
        self.rect = QRect(self.bottom, self.top)
        self.setGeometry(self.rect)
        self.cc_click_action = (PicPicAttrGen, self.core)
        self.attr_widgets = []
        self.clicked.connect(self.click_button)

    def click_button(self):
        ret = self.cc_click_action[0](self.cc_click_action[1])
        self.attr_widgets = ret
        self.signal.fired.emit(self.attr_widgets)

    def paintEvent(self, *args, **kwargs):
        super(PicPicButton, self).paintEvent(*args, **kwargs)
        self.setText(self.core.name.value)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            proxy = self.graphicsProxyWidget()
            self.signal.deleted.emit([proxy])
            del proxy
        QPushButton.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.move(self.mapToParent(event.pos()))
        QPushButton.mouseMoveEvent(self, event)
        
class PicPicLayer(PicPicShape):
    def __init__(self, bottom, top, core):
        super(PicPicLayer, self).__init__(core=core)
        self.bottom = bottom
        self.top = top
        self.rect = QRect(self.bottom, self.top)
        self.bb_rect = self.rect
        self.adjust_rect = self.rect.adjusted(self.rect.width()+5,0,self.rect.width()/4.0,0)
    
    def paint(self, painter, option, widget):
        super(PicPicLayer, self).paint(painter, option, widget)
        painter.drawRoundedRect(self.rect, 10, 10)
        painter.drawRoundedRect(self.adjust_rect, 10, 10)
        painter.drawRoundedRect(self.adjust_rect.adjusted(self.adjust_rect.width() + 5, 0, self.rect.width() / 4.0, 0), 10, 10)
        self.bb_rect = QRect(self.rect.topLeft(), self.adjust_rect.bottomRight())
