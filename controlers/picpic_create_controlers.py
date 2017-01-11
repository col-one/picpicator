from PySide.QtCore import *
from PySide.QtGui import *
import copy

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
        self.btn_1 = PicPicButton(".", self)
        self.btn_2 = PicPicButton(".", self)
        self.btn_3 = PicPicButton(".", self)
        #attributes
        self.buttons = [self.rect_btn, self.circle_btn, self.free_btn,
                        self.btn_1, self.btn_2, self.btn_3]
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
        self.btn_1.clicked.connect(self.click_btn_1)

    def click_rect_btn(self):
        pass
    def click_circle_btn(self):
        pass
    def click_free_btn(self):
        pass
    def click_btn_1(self):
        pass

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
        self.plain_rect.adjust(+30,+30,-30,-30)
        self.color = QColor(255,200,0,255)
        self.plain_color = QColor(255,255,255,255)

    def boundingRect(self, *args, **kwargs):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRect(self.rect)
        painter.setBrush(self.plain_color)
        painter.drawRect(self.plain_rect)

class PicPicBrushBtn(QGraphicsItem):
    def __init__(self, rect):
        super(PicPicBrushBtn, self).__init__()
        self.rect = rect
        self.plain_rect = copy.deepcopy(self.rect)
        self.plain_rect.adjust(+30, +30, -30, -30)
        self.color = QColor(04, 200, 0, 255)
        self.plain_color = QColor(255, 255, 255, 255)

    def boundingRect(self, *args, **kwargs):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.plain_color)
        painter.drawRect(self.rect)
        painter.setBrush(self.color)
        painter.drawRect(self.plain_rect)




#
# if __name__ == '__main__':
#
#     import sys
#     app = QApplication(sys.argv)
#     window = PicPicColorUi()
#     window.resize(640, 480)
#     window.show()
# sys.exit(app.exec_())