from PySide.QtCore import *
from PySide.QtGui import *

class PicSignal(QObject):
    changed = Signal(list)

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        # self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(0)
        self.setContentsMargins(0,0,0,0)

class PicPicColorPicker(QColorDialog):
    def __init__(self, parent):
        super(PicPicColorPicker, self).__init__(parent)
        self.setOption(QColorDialog.DontUseNativeDialog)
        self.currentColorChanged.connect(self.change_color)
        self.color = QColor(255,255,255)
        self.show()

    def implementation_change(self):
        pass

    def change_color(self, color):
        self.color = color
        self.implementation_change()


class PicPicAbstract(QWidget):
    def __init__(self, properties, label):
        super(PicPicAbstract, self).__init__()
        self.signal = PicSignal()
        self.value = properties.value
        self.label_name = label
        self.expo_order = properties.expo_order
        self.properties = properties

class PicPicString(PicPicAbstract):
    def __init__(self, properties, label):
        super(PicPicString, self).__init__(properties, label)

        self.label = QLabel(self.label_name + " : ")
        self.text_edit = QLineEdit(self.value)
        self.sep = QHLine()

        self.lay = QVBoxLayout(self)
        self.lay.addWidget(self.label)
        self.lay.addWidget(self.text_edit)
        self.lay.addWidget(self.sep)

        self.lay.setSpacing(1)
        self.setMinimumWidth(190)

        self.text_edit.textChanged.connect(self.send_signal)

    def send_signal(self):
        self.properties.value = self.text_edit.text()


class PicPicFloat(PicPicAbstract):
    def __init__(self, properties, label):
        super(PicPicFloat, self).__init__(properties, label)
        self.signal = PicSignal()
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
        self.properties.value = float(self.integer.text())

    def linkInt(self):
        self.slider.setValue(int(self.integer.text()))
        self.properties.value = float(self.integer.text())

class PicPicColor(PicPicAbstract):
    def __init__(self, properties, label):
        super(PicPicColor, self).__init__(properties, label)
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

        self.button.clicked.connect(self.send_signal)

    def send_signal(self):
        color_pick = PicPicColorPicker(self)
        def set_color(color):
            self.properties.value = color
            self.color_hex = color.name()
            self.button.setStyleSheet("background-color:{0}; border: 0px".format(self.color_hex))
        color_pick.implementation_change = lambda *args : set_color(color_pick.color)


# import sys
# app = QApplication(sys.argv)
# v = picpic_entities.Property()
# v.value = QColor(255,0,255)
# d = PicPicColor(v, "name")
# d.show()
# sys.exit(app.exec_())
