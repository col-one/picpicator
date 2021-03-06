from PySide.QtCore import *
from PySide.QtGui import *
import copy

from entities import picpic_entities
from controlers import picpic_shape_controlers, picpic_properties_controlers

CIRCLE = 'Circle Tool'
SQUARE = 'Square Tool'
FREE = 'Free Tool'
TEXT = 'Text Tool'
BUTTON = 'Button Tool'
LAYER = 'Layer Tool'

class PicPicButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(PicPicButton, self).__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumSize(QSize(5,5))

    def is_checkable(self, layout):
        count = layout.count()
        for i in range(0, count):
            widget = layout.itemAt(i)
            if widget.widget().isChecked():
                return False
        return True

    def hitButton(self, *args, **kwargs):
        super(PicPicButton, self).hitButton(*args, **kwargs)
        if self.is_checkable(self.parentWidget().grid_layout):
            self.setCheckable(True)
            return True
        else:
            self.setCheckable(False)
            return False

class PicPicToolsUi(QWidget):
    def __init__(self):
        super(PicPicToolsUi, self).__init__()
        #widgets
        #must be at the top layout
        self.grid_layout = QGridLayout(self)
        self.rect_btn = PicPicButton()
        self.rect_btn.setIcon(QIcon("icones/square-outlined-shape.png"))
        self.circle_btn = PicPicButton()
        self.circle_btn.setIcon(QIcon("icones/circle-outline.png"))
        self.free_btn = PicPicButton()
        self.free_btn.setIcon(QIcon("icones/pencil.png"))
        self.text_btn = PicPicButton()
        self.text_btn.setIcon(QIcon("icones/text.png"))
        self.btn_btn = PicPicButton()
        self.btn_btn.setIcon(QIcon("icones/add.png"))
        self.layer_btn = PicPicButton()
        self.layer_btn.setIcon(QIcon("icones/layers.png"))        #attributes
        self.buttons = [self.rect_btn, self.circle_btn, self.free_btn,
                        self.text_btn, self.btn_btn, self.layer_btn]
        self.active_button = False
        #laying
        self.grid_layout.addWidget(self.buttons[0], 0, 0, 0)
        self.grid_layout.addWidget(self.buttons[1], 0, 1, 0)
        self.grid_layout.addWidget(self.buttons[2], 0, 2, 0)
        self.grid_layout.addWidget(self.buttons[3], 1, 0, 0)
        self.grid_layout.addWidget(self.buttons[4], 1, 1, 0)
        self.grid_layout.addWidget(self.buttons[5], 1, 2, 0)
        #overide
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.setFixedSize(200, 125)
        #connect
        self.rect_btn.clicked.connect(self.click_rect_btn)
        self.circle_btn.clicked.connect(self.click_circle_btn)
        self.free_btn.clicked.connect(self.click_free_btn)
        self.text_btn.clicked.connect(self.click_text_btn)
        self.btn_btn.clicked.connect(self.click_btn_btn)
        self.layer_btn.clicked.connect(self.click_layer_btn)

    def mousePressEvent(self, e):
        self.info_from_click()
        self.active_button = not self.active_button
        self.current_view.active_tool = None
        QWidget.mousePressEvent(self, e)

    def info_from_click(self):
        self.current_view = self.window().tab.core[self.window().tab.currentIndex()].view

    def click_rect_btn(self):
        self.info_from_click()
        if not self.active_button:
            self.current_view.active_tool = SQUARE
            self.active_button = not self.active_button

    def click_circle_btn(self):
        self.info_from_click()
        if not self.active_button:
            self.current_view.active_tool = CIRCLE
            self.active_button = not self.active_button

    def click_free_btn(self):
        self.info_from_click()
        if not self.active_button:
            self.current_view.active_tool = FREE
            self.active_button = not self.active_button
            free_core = picpic_entities.PicPicFreeCore()
            self.current_view.free_shape = picpic_shape_controlers.PicPicFreeDraw(free_core)
            self.current_view.free_node = picpic_shape_controlers.PicPicNode(self.current_view.free_shape)

    def click_text_btn(self):
        self.info_from_click()
        if not self.active_button:
            self.current_view.active_tool = TEXT
            self.active_button = not self.active_button

    def click_btn_btn(self):
        self.info_from_click()
        if not self.active_button:
            self.current_view.active_tool = BUTTON
            self.active_button = not self.active_button

    def click_layer_btn(self):
        self.info_from_click()
        if not self.active_button:
            self.current_view.active_tool = LAYER
            self.active_button = not self.active_button


    def uncheck_all(self):
        for btn in self.buttons:
            btn.setChecked(False)
        self.active_button = False

class PicPicColorUi(QWidget):
    def __init__(self):
        super(PicPicColorUi, self).__init__()
        #widget
        self.view = QGraphicsView(self)
        self.view.resize(200,100)
        self.scene_ = QGraphicsScene(self)
        self.scene_.setSceneRect(0, 0, 200, 100)
        #
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #
        self.view.setScene(self.scene_)

        self.pen_btn = PicPicPenBtn(QRect(-1,-1,101,101))
        self.brush_btn = PicPicBrushBtn(QRect(100,-1,101,101))
        self.view.scene().addItem(self.pen_btn)
        self.view.scene().addItem(self.brush_btn)
        #
        self.setFixedSize(200, 100)

class PicPicPenBtn(QGraphicsItem):
    def __init__(self, rect):
        super(PicPicPenBtn, self).__init__()
        self.rect = rect
        self.plain_rect = copy.deepcopy(self.rect)
        self.plain_rect.adjust(+15,+15,-15,-15)
        self.color = QColor(35,45,200)
        self.plain_color =  QColor(255,255,255)
        self.color_dial = picpic_properties_controlers.PicPicColorPicker(self.window())
        self.color_dial.setCurrentColor(self.color)
        self.color_dial.currentColorChanged.connect(self.change_color)

    def change_color(self, color):
        self.color = color

    def boundingRect(self, *args, **kwargs):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRect(self.rect)
        painter.setBrush(self.plain_color)
        painter.drawRect(self.plain_rect)

    def mousePressEvent(self, e):
        self.color_dial.show()
        QGraphicsItem.mousePressEvent(self, e)


class PicPicBrushBtn(QGraphicsItem):
    def __init__(self, rect):
        super(PicPicBrushBtn, self).__init__()
        self.rect = rect
        self.plain_rect = copy.deepcopy(self.rect)
        self.plain_rect.adjust(+15, +15, -15, -15)
        self.color = QColor(04, 200, 0, 255)
        self.plain_color = QColor(255, 255, 255, 255)
        self.color_dial = picpic_properties_controlers.PicPicColorPicker(self.window())
        self.color_dial.setCurrentColor(self.color)
        self.color_dial.currentColorChanged.connect(self.change_color)

    def change_color(self, color):
        self.color = color

    def boundingRect(self, *args, **kwargs):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.plain_color)
        painter.drawRect(self.rect)
        painter.setBrush(self.color)
        painter.drawRect(self.plain_rect)

    def mousePressEvent(self, e):
        self.color_dial.show()
        QGraphicsItem.mousePressEvent(self, e)



# if __name__ == '__main__':
#
#     import sys
#     app = QApplication(sys.argv)
#     window = PicPicColorUi()
#     window.resize(640, 480)
#     window.show()
# sys.exit(app.exec_())