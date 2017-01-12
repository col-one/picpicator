from PySide.QtCore import *
from PySide.QtGui import *


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        # self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(0)
        self.setContentsMargins(0,0,0,0)

class PicPicString(QWidget):
    def __init__(self, properties, label):
        super(PicPicString, self).__init__()
        self.value = properties.value
        self.label_name = label

        self.label = QLabel(self.label_name + " : ")
        self.text_edit = QLineEdit()
        self.sep = QHLine()

        self.lay = QVBoxLayout(self)
        self.lay.addWidget(self.label)
        self.lay.addWidget(self.text_edit)
        self.lay.addWidget(self.sep)

        self.lay.setSpacing(1)
        self.setMinimumWidth(190)

        #self.setStyleSheet("color: #999999")


class PicPicFloat(QWidget):
    def __init__(self, properties, label):
        super(PicPicFloat, self).__init__()
        self.property = properties
        self.value = properties.value
        self.label_name = label

        self.label = QLabel(self.label_name + " : ")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(int(self.value))
        self.integer = QLineEdit(str(self.value))
        self.integer.setValidator(QIntValidator(0, 100))
        self.integer.setMaximumWidth(40)
        self.sep = QHLine()
        self.sep2 = QHLine()

        self.lay = QGridLayout(self)
        self.lay.addWidget(self.label, 0, 0)
        self.lay.addWidget(self.slider, 1, 0)
        self.lay.addWidget(self.integer, 1, 1)
        self.lay.addWidget(self.sep, 2, 0)
        self.lay.addWidget(self.sep2, 2, 1)

        self.lay.setSpacing(1)
        self.setMinimumWidth(190)

        #self.setStyleSheet("color: #999999")

        self.slider.valueChanged.connect(self.link)
        self.integer.textChanged.connect(self.linkInt)

    def link(self):
        self.integer.setText(str(self.slider.value()))
        self.property.value = self.integer.text()
    def linkInt(self):
        self.slider.setValue(int(self.integer.text()))
        self.property.value = self.integer.text()

class PicPicColor(QWidget):
    def __init__(self, properties, label):
        super(PicPicColor, self).__init__()
        self.property = properties
        self.value = properties.value
        self.label_name = label
        if not isinstance(self.value, QColor):
            self.value = QColor(*self.value)
        self.color_hex = self.value.name()

        self.label = QLabel(self.label_name + " : ")
        self.button = QPushButton()
        self.button.setStyleSheet("background-color:{0}; border: 0px".format(self.color_hex))
        self.sep = QHLine()

        self.lay = QVBoxLayout(self)
        self.lay.addWidget(self.label)
        self.lay.addWidget(self.button)
        self.lay.addWidget(self.sep)


        self.lay.setSpacing(1)
        self.setMinimumWidth(190)

        #self.setStyleSheet("color: #999999")

# import sys
# app = QApplication(sys.argv)
# v = picpic_entities.Property()
# v.value = QColor(255,0,255)
# d = PicPicColor(v, "name")
# d.show()
# sys.exit(app.exec_())
