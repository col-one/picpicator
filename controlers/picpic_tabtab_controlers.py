from PySide.QtCore import *
from PySide import *

class TabBarPlus(QtGui.QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    plusClicked = QtCore.Signal()

    def __init__(self):
        super(TabBarPlus, self).__init__()
        # Plus Button
        self.plusButton = QtGui.QPushButton("+")
        self.plusButton.setParent(self)
        self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(20, 20) # Small Fixed size
        self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton() # Move to the correct location
    # end Constructor

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QtGui.QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QtCore.QSize(width+25, height)
    # end tabSizeHint

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super(TabBarPlus, self).resizeEvent(event)
        self.movePlusButton()
    # end resizeEvent

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the plus button is in the correct location.
        """
        super(TabBarPlus, self).tabLayoutChange()
        self.movePlusButton()
    # end tabLayoutChange

    def movePlusButton(self):
        """Move the plus button to the correct location."""
        # Find the width of all of the tabs
        size = 0
        for i in range(self.count()):
            size += self.tabRect(i).width()

        # Set the plus button location in a visible area
        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            self.plusButton.move(w-54, h)
        else:
            self.plusButton.move(size+3, h)
    # end movePlusButton
# end class MyClass

class CustomTabWidget(QtGui.QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""

    def __init__(self):
        super(CustomTabWidget, self).__init__()
        # Tab Bar
        self.tab = TabBarPlus()
        self.setTabBar(self.tab)

        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)

        # Signals
        self.tab.plusClicked.connect(self.add_tab)
        #self.tab.tabMoved.connect(self.moveTab)
        self.tabCloseRequested.connect(self.removeTab)

    def add_tab(self):
        w = QtGui.QWidget()
        self.addTab(w, 'toto')

class PicPicTab(QtGui.QWidget):
    def __init__(self):
        super(PicPicTab, self).__init__()
        l = QtGui.QVBoxLayout(self)
        d = CustomTabWidget()
        w = QtGui.QWidget()
        d.addTab(w, "dsds")
        l.addWidget(d)

import sys
app = QtGui.QApplication(sys.argv)
d = PicPicTab()
d.show()
sys.exit(app.exec_())

