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
        self.addTab(self.core[-1].wrapper, self.core[self.id].name.value)
        self.core[-1].wrapper.id = self.id
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
            self.wid = picpic_view_controlers.PicPicWrapper(view=self.view)
            if window:
                self.window = window
            self.scene_.editor = self.window.editor
            self.scene_.add_background(fileName[0])
            pic_core_dict = PicTabDict(view=self.view)
            pic_core_dict.image.value = fileName
            pic_core_dict.wrapper = self.wid
            self.scene_.picpic_dict = pic_core_dict
            self.add_tab(pic_core_dict)
            self.window.setCentralWidget(self)


class PicPicData(object):
    def __init__(self):
        self.tabs = []
        self.layers = []
        self.shapes = []

class PicPicTabCore(object):
    def __init__(self):
        self.name = ''
        self.id = 0
        self.bck = ''

class PicPicLayerCore(object):
    def __init__(self):
        self.name = ''
        self.id = 0
        self.parent_tab_id = 0


class PicPicShapeCore(object):
    def __init__(self):
        super(PicPicShapeCore, self).__init__()
        self.name = Property("Shape")
        self.name.type = STRING
        self.name.expo_order = 0
        self.action = Property("")
        self.action.type = STRING
        self.action.expo_order = 0.1
        self.color = Property((122,11,11,255))
        self.color.type = COLOR
        self.color.expo_order = 1
        self.pen_color = Property((125,55,44))
        self.pen_color.type = COLOR
        self.pen_color.expo_order = 2
        self.over_color = Property((122,78,45,255))
        self.over_color.type = COLOR
        self.over_color.expo_order = 3
        self.opacity = Property(50.0)
        self.opacity.type = FLOAT
        self.click_color = Property((120,200,255))
        self.click_color.type = COLOR
        self.click_color.expo_order = 4
        self.vertex = Property()
        self.vertex.type = LIST
        self.vertex.expo = False
        self.selected = None
        self.pen_width = Property(0.1)
        self.pen_width.type = FLOAT
        self.pen_width.expo_order = 5
        self.scale = Property(1.0)
        self.scale.type = FLOAT
        self.rotate = Property(0.0)
        self.rotate.type = FLOAT





