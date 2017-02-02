import sys
import copy
from PySide.QtCore import *
from PySide.QtGui import *

from controlers import picpic_shape_controlers, picpic_create_controlers, picpic_editor_controlers, \
    picpic_view_controlers, picpic_tabtab_controlers
from controlers.picpic_editor_controlers import PicPicAttrGen
from entities import picpic_entities


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("PicPicator")
        self.statusBar().showMessage("PicPicator is launching... OK")
        #quit
        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)
        #save
        self.saveAction = QAction('&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save .pic file')
        #self.saveAction.triggered.connect(self.save)
        #save as
        self.saveAsAction = QAction('&Save as...', self)
        self.saveAsAction.setShortcut('Ctrl+Shift+S')
        self.saveAsAction.setStatusTip('Save as .pic file')
        #self.saveAsAction.triggered.connect(self.close)

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.exitAction)


        self.create = picpic_create_controlers.PicPicToolsUi()
        self.color = picpic_create_controlers.PicPicColorUi()
        self.editor = picpic_editor_controlers.PicPicFrame()

        self.tab_core = picpic_entities.PicPicTabCore()
        fist_tab = picpic_entities.PicTabDict()
        self.tab_core.append(fist_tab)
        self.tab = picpic_tabtab_controlers.PicPicTab(core=self.tab_core)
        self.tab.add_tab()

        self.setCentralWidget(self.tab)

        self.dock = QDockWidget("Tools")
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dock.setWidget(self.create)

        self.dock_color = QDockWidget("Colors")
        self.dock_color.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dock_color.setWidget(self.color)

        self.dock_prop = QDockWidget("Shapes Properties")
        self.dock_prop.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dock_prop.setWidget(self.editor)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_color)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_prop)

        #
        core = picpic_entities.PicPicShapeCore()
        self.circle = picpic_shape_controlers.PicPicRect(QPoint(-150, -150), QPoint(150, 150), core=core)
        self.node = picpic_shape_controlers.PicPicNode(self.circle)

        #self.scene_.add_picpicitem(self.node)
        #
        # widget_right = QWidget(self)
        # lay_right = QVBoxLayout(widget_right)
        # lay_right.addWidget(create_lay)
        # lay_right.addWidget(color_lay)
        # lay_right.addWidget(self.editor)
        #
        # layout = QHBoxLayout(self)
        # layout.addWidget(self.view)
        # layout.addWidget(widget_right)

    #     self.view.scene().items()[0].signal.fired.connect(self.pop)
    #
    # @Slot(list)
    # def pop(self, event):
    #     self.editor.populate_attr(event)

    # def handleClearView(self):
    #     shape_core = picpic_entities.PicPicFreeCore()
    #     shape = picpic_shape_controlers.PicPicFreeDraw(core=shape_core)
    #     self.view.shape.append(shape)
    #     self.view.id += 1
    #     self.view.scene().addItem(self.view.shape[self.view.id])
    #     shape.setParentItem(self.view.bck)
    #     self.view.start_draw = True
    #
    # def change_opacity(self):
    #     #for item in self.view.scene().selectedItems():
    #     #    print item.color
    #     #n_color = self.view.scene().selectedItems()[0].color
    #     new_color = self.view.scene().selectedItems()[0].color
    #     new_color.setAlpha(255-self.opacity.value())
    #     self.view.scene().selectedItems()[0].color = new_color
    #     #self.view.scene().selectedItems()[0].color = new_color

# class View(QGraphicsView):
#     def __init__(self, parent):
#         QGraphicsView.__init__(self, parent)
#         self.setRenderHint(QPainter.Antialiasing)
#         self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#         self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
#         self.setBackgroundBrush(QColor(70, 70, 70))
#         self.setDragMode(QGraphicsView.RubberBandDrag)
#         self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # self.bck = QGraphicsPixmapItem()
        # self.img = QPixmap("./Jadina_Fond.jpg")
        # self.bck.setPixmap(self.img)
        # self.bck.setZValue(-1000)
        # self.bck.setOffset( -0.5 * QPointF( self.img.width(), self.img.height() ) )



        # self.setMaximumHeight(self.img.height())
        # self.setMinimumHeight(self.img.height())
        # self.setMaximumWidth(self.img.width())
        # self.setMinimumWidth(self.img.width())

        # self.scene_ = QGraphicsScene()
        # self.scene_.setSceneRect(-50000, -50000, 100000, 100000)
        # self.setScene(self.scene_)
        # self.scene_.addItem(self.bck)
        # self.scene_.addItem(self.node)




    # def mousePressEvent(self, event):
    #     self.parent().editor.delete_attr_panel()
    #     if not self.start_draw:
    #         return QGraphicsView.mousePressEvent(self, event)
    #     if len(self.shape[self.id].core.vertex) == 0:
    #         self.shape[self.id].start_draw(self.mapToScene(event.pos()))
    #         #self.shape[self.id].set_bounding(self.mapToScene(event.pos()))
    #     else:
    #         self.shape[self.id].add_line(self.mapToScene(event.pos()))
    #     QGraphicsView.mousePressEvent(self, event)

    # def keyPressEvent(self, event):
    #     super(View, self).keyPressEvent(event)
    #     if event.key() == Qt.Key_Return:
    #         self.shape[self.id].end_draw()
    #         self.start_draw = False
    #         print self.shape[self.id].vertex

# class Shape(QGraphicsItem):
#     def __init__(self):
#         super(Shape, self).__init__()
#         self.setFlags(
#             QGraphicsItem.ItemIsFocusable |
#             QGraphicsItem.ItemIsSelectable |
#             QGraphicsItem.ItemIsMovable |
#             QGraphicsItem.ItemSendsGeometryChanges
#         )
#
#         self.setAcceptHoverEvents(True)
#         self.setSelected(True)
#
#         self.rect = QRect()
#         self.first_point = True
#         self.path_draw = QPainterPath()
#         self.color = QColor(0.0, 220.0, 0.0)
#         self.light_color = self.color.lighter(150)
#         self.begin_point = None
#         self.vertex = []
#         self.closed = False
#         self.over = False
#         self.rect = QRect(0,0,50,50)
#         self.over_color = QColor(255, 255, 255, 150)
#         self.select_color = QColor(255, 255, 255, 100)
#
#     def get_color(self):
#         return self.color
#
#     def set_color(self, color):
#         self.color = color
#
#     def set_bounding(self, click):
#         click = self.mapToScene(click)
#         #self.rect = QRect(click.x(), click.y(), 50, 50)
#
#     def start_point(self, point):
#         self.begin_point = point
#         self.path_draw.moveTo(point)
#         self.first_point = False
#         self.vertex.append(point)
#
#     def add_point(self, point):
#         self.path_draw.lineTo(point)
#         self.vertex.append(point)
#
#     def close_path(self):
#         self.path_draw.closeSubpath()
#         self.closed = True
#         self.setSelected(True)
#         self.setActive(True)
#         self.rect = self.mapRectToScene(self.path_draw.controlPointRect())
#
#     def boundingRect(self):
#         return self.rect
#
#     def paint(self, painter, option, widget):
#         if self.over:
#             painter.setPen(self.over_color)
#             painter.drawRect(self.rect)
#         elif self.isSelected():
#             painter.setPen(self.select_color)
#             painter.drawRect(self.rect)
#             #
#             # painter.setBrush(self.light_color)
#             # painter.setBrush(self.light_color)
#         painter.setPen(self.color)
#         painter.setBrush(self.color)
#         painter.drawPath(self.path_draw)
#         painter.setPen(QColor(255,0,0))
#         painter.setBrush(Qt.NoBrush)
#         #painter.drawRect(self.path_draw.controlPointRect())
#         self.scene().update()
#
#     def hoverEnterEvent(self, event):
#         self.over = True
#         self.scene().update()
#     def hoverLeaveEvent(self, event):
#         self.over = False
#         self.scene().update()


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = Window()
    window.resize(640, 480)
    window.show()
sys.exit(app.exec_())