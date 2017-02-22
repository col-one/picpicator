from PySide.QtCore import *
from PySide.QtGui import *
import copy

from entities.picpic_entities import *


class RoundButton(QPushButton):
    def __init__(self):
        super(RoundButton, self).__init__()
        self.setText("Test Text")
        self.setFixedHeight(200)
        self.setFixedWidth(200)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = RoundButton()
    window.show()
sys.exit(app.exec_())
