from PySide.QtCore import *
from PySide.QtGui import *

class PicPicButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(PicPicButton, self).__init__(*args, **kwargs)

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




class PicPicCreateUi(QWidget):
    def __init__(self):
        super(PicPicCreateUi, self).__init__()
        #widgets
        #must be at the top
        self.grid_layout = QGridLayout(self)
        self.rect_btn = PicPicButton("r", self)
        self.circle_btn = PicPicButton("c", self)
        self.free_btn = PicPicButton("d", self)
        self.btn = PicPicButton(".", self)
        self.btn = PicPicButton(".", self)
        self.btn = PicPicButton(".", self)

        #attributes
        self.buttons = [self.rect_btn, self.circle_btn, self.free_btn,
                        self.btn, self.btn, self.btn]

        #laying
        i = 0
        for x in [0,2]:
            for y in [0,2]:
                self.grid_layout.addWidget(self.buttons[i], x, y)
                i += 1

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = PicPicCreateUi()
    window.resize(640, 480)
    window.show()
sys.exit(app.exec_())