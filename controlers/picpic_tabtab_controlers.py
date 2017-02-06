from PySide.QtCore import *
from PySide.QtGui import *\

from controlers import picpic_view_controlers
from entities.picpic_entities import *

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
    def __init__(self, core=PicPicTabCore):
        super(PicPicTab, self).__init__()
        self.core = core
        self.tab = TabBarPlus()
        self.setTabBar(self.tab)
        self.setMovable(True)
        self.setTabsClosable(True)

        self.tab.plusClicked.connect(self.add_tab_background)
        self.tabCloseRequested.connect(self.remove_tab)
        self.id = self.currentIndex()

    def add_tab(self, pic_dict):
        self.id += 1
        self.core.append(pic_dict)
        self.addTab(self.core[-1].view, self.core[self.id].name.value)
        self.adjustSize()

    def remove_tab(self, e):
        if self.tab.count() == 1:
            return
        self.id -= 1
        del self.core[self.currentIndex()]
        self.removeTab(e)
        self.window.adjustSize()


    def add_tab_background(self, window=None):
        #tab = self.window().tab
        dialog = QFileDialog()
        dialog.setViewMode(QFileDialog.Detail)
        fileName = QFileDialog.getOpenFileName(self, "Open File", "Image")
        if fileName[0] != '':
            self.scene_ = picpic_view_controlers.PicPicScene()
            self.view = picpic_view_controlers.PicPicView(scene=self.scene_)
            if window:
                self.window = window
            self.scene_.editor = self.window.editor
            self.scene_.add_background(fileName[0])
            pic_core_dict = PicTabDict(view=self.view)
            pic_core_dict.image.value = fileName
            self.add_tab(pic_core_dict)
            self.window.setCentralWidget(self)