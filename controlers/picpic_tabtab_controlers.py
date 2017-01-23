from PySide.QtCore import *
from PySide.QtGui import *\

from controlers import picpic_view_controlers

class TabBarPlus(QTabBar):

    plusClicked = Signal()

    def __init__(self):
        super(TabBarPlus, self).__init__()
        self.plusButton = QPushButton("+")
        self.plusButton.setParent(self)
        self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(20, 20) # Small Fixed size
        self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton()

    def sizeHint(self):
        sizeHint = QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QSize(width+25, height)

    def resizeEvent(self, event):
        super(TabBarPlus, self).resizeEvent(event)
        self.movePlusButton()

    def tabLayoutChange(self):
        super(TabBarPlus, self).tabLayoutChange()
        self.movePlusButton()

    def movePlusButton(self):
        size = 0
        for i in range(self.count()):
            size += self.tabRect(i).width()

        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            self.plusButton.move(w-54, h)
        else:
            self.plusButton.move(size+3, h)

    def mouseDoubleClickEvent(self, event):
        idx = self.currentIndex()
        ok = True
        newName = QInputDialog.getText(self, "Rename tab", "Insert New Tab Name", QLineEdit.Normal, self.tabText(idx), ok)
        if ok:
            self.setTabText(idx, newName[0])
            self.window().statusBar().showMessage("Tab is rename '{0}'".format(newName[0]), 2500)

class PicPicTab(QTabWidget):
    def __init__(self):
        super(PicPicTab, self).__init__()
        self.tab = TabBarPlus()
        self.setTabBar(self.tab)
        self.setMovable(True)
        self.setTabsClosable(True)

        self.tab.plusClicked.connect(self.add_tab)
        self.tabCloseRequested.connect(self.removeTab)

    def add_tab(self):
        widget = picpic_view_controlers.PicPicEmptyView()
        self.addTab(widget, 'main (click to rename)')

# class PicPicTab(QWidget):
#     def __init__(self):
#         super(PicPicTab, self).__init__()
#         l = QVBoxLayout(self)
#         d = CustomTabWidget()
#         l.addWidget(d)

# import sys
# app = QApplication(sys.argv)
# d = PicPicTab()
# d.show()
# sys.exit(app.exec_())

