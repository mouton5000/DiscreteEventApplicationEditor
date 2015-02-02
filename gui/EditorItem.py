from gui.LabelItems import LabelItem

__author__ = 'mouton'


from PyQt4 import QtCore
from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsView, QGraphicsScene
from undoRedoActions import *
from NodeItems import NodeItem, ConnectedComponent
from ArcItems import ArcItem, CycleArcItem
from collections import deque


class ViewWidget(QGraphicsView):

    DEFAULT_X = -200
    DEFAULT_Y = -200
    DEFAULT_W = 400
    DEFAULT_H = 400

    def __init__(self, parent=None, mainWindow=None, nodesIdsGenerator=None, modeController=None):
        super(ViewWidget, self).__init__(parent)
        self.mainWindow = mainWindow
        self._tabIndex = None
        scene = SceneWidget(self, mainWindow=self.mainWindow, nodesIdsGenerator=nodesIdsGenerator,
                            modeController=modeController)
        self.setScene(scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rect = QRectF(ViewWidget.DEFAULT_X, ViewWidget.DEFAULT_Y, ViewWidget.DEFAULT_W, ViewWidget.DEFAULT_H)
        self.setSceneRect(self.rect)
        self.px = None
        self.py = None
        self.propertiesEditor = None
        self.scl = 1

    def showTab(self):
        tabItem = self.mainWindow.centralWidget().tabItem()
        tabItem.showTabbedView(self)

    def wheelEvent(self, event):
        step = event.delta() / 120
        scale = 1.1 ** step
        self.scale(scale, scale)
        self.scl *= scale

    def mouseMoveEvent(self, event):
        item = self.scene().mouseGrabberItem()
        if item:
            super(ViewWidget, self).mouseMoveEvent(event)
        else:
            x, y = event.x(), event.y()
            if self.px:
                self.translate((x - self.px) / self.scl, (y - self.py) / self.scl)

            self.px = x
            self.py = y

    def mouseReleaseEvent(self, event):
        if self.px:
            self.px = None
            self.py = None
        else:
            super(ViewWidget, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        dx, dy = 0, 0
        if event.key() == QtCore.Qt.Key_Right:
            dx, dy = -30, 0
        elif event.key() == QtCore.Qt.Key_Left:
            dx, dy = 30, 0
        elif event.key() == QtCore.Qt.Key_Up:
            dx, dy = 0, 30
        elif event.key() == QtCore.Qt.Key_Down:
            dx, dy = 0, -30
        if dx != 0 or dy != 0:
            self.translate(dx, dy)
            return
        if event.key() == QtCore.Qt.Key_F:
            self.center()
        else:
            super(ViewWidget, self).keyPressEvent(event)

    def translate(self, dx, dy):
        self.rect.translate(-dx, -dy)
        self.setSceneRect(self.rect)

    def center(self):
        scale = self.scl
        self.scale(1 / scale, 1 / scale)
        self.scl = 1
        self.translate(self.rect.x() - ViewWidget.DEFAULT_X, self.rect.y() - ViewWidget.DEFAULT_Y)

    def setPropertiesEditor(self, pe):
        self.propertiesEditor = pe


class SceneWidget(QGraphicsScene):
    def __init__(self, parent=None, mainWindow=None, nodesIdsGenerator=None, modeController=None):
        super(SceneWidget, self).__init__(parent)
        self.nodesIdsGenerator = nodesIdsGenerator
        self.mainWindow = mainWindow
        self.modeController = modeController
        self.init()

    def init(self):
        self.nodes = []
        self._selected = None
        self.setNodeMode()
        self.setName('unnamed')

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
        self.mainWindow.centralWidget().tabItem().setTabbedViewText(self.parent(), name)

    def addItem(self, item):
        super(SceneWidget, self).addItem(item)
        try:
            item.add()
        except AttributeError:
            pass

    def clear(self):
        super(SceneWidget, self).clear()
        self.init()

    def getNextNodeId(self):
        return self.nodesIdsGenerator.getNextNodeId()

    def removeNodeIndex(self, index):
        self.nodesIdsGenerator.removeNodeIndex(index)

    def addNode(self, x, y):
        num = self.getNextNodeId()
        node = NodeItem(x, y, num, scene=self)
        self.setSelected(node)
        # Apparently, addItem is not called when an item is created
        node.add()
        return node

    def getCloseNodeOf(self, x, y):
        for node in self.nodes:
            if node.isCloseTo(x, y):
                return node

    def addArc(self, n1, n2):
        if n1 == n2:
            arc = CycleArcItem(n1, scene=self)
        else:
            arc = ArcItem(n1, n2, scene=self)
        if self.isPathMode():
            self.setSelected(n2)
        return arc

    def mousePressEvent(self, event):
        super(SceneWidget, self).mousePressEvent(event)
        item = self.mouseGrabberItem()
        if item is not None and self._selected is not None and self.isComponentMode() and item in self._selected:
            x, y = event.scenePos().x(), event.scenePos().y()
            self._selected.initMove(x, y)

    def mouseMoveEvent(self, event):
        item = self.mouseGrabberItem()
        if item and self._selected and self.isComponentMode() and item in self._selected:
            x, y = event.scenePos().x(), event.scenePos().y()
            self._selected.move(x, y)
        else:
            super(SceneWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        item = self.mouseGrabberItem()
        if self.isNodeMode():
            if not item:
                x, y = event.scenePos().x(), event.scenePos().y()
                self.addNode(x, y)
            elif isinstance(item, NodeItem):
                self.setSelected(item)
                item.mouseReleaseEvent(event)
            elif isinstance(item, LabelItem):
                self.setSelected(item.labelOf)
                item.mouseReleaseEvent(event)
            else:
                item.mouseReleaseEvent(event)
        elif self.isArcMode():
            if not item:
                self.setSelected(None)
            else:
                if isinstance(item, NodeItem):
                    if isinstance(self._selected, NodeItem):
                        self.addArc(self._selected, item)
                    else:
                        self.setSelected(item)
                elif isinstance(item, ArcItem):
                    self.setSelected(item)
                elif isinstance(item, LabelItem):
                    self.setSelected(item.labelOf)
                item.mouseReleaseEvent(event)
        elif self.isSeparateInputMode() or self.isSeparateOutputMode():
            if not item:
                self.setSelected(None)
            elif isinstance(item, ArcItem):
                self.setSelected(item)
                item.mouseReleaseEvent(event)
            else:
                item.mouseReleaseEvent(event)
        elif self.isSelectMode():
            if item:
                if not isinstance(item, LabelItem):
                    self.setSelected(item)
                else:
                    self.setSelected(item.labelOf)
                item.mouseReleaseEvent(event)
        elif self.isComponentMode():
            if self._selected:
                x, y = event.scenePos().x(), event.scenePos().y()
                self._selected.endMove(x, y)
                if item:
                    item.mouseReleaseEvent(event)
            else:
                if item:
                    try:
                        self.setSelected(item.getConnectedComponent())
                    except AttributeError:
                        pass
                    item.mouseReleaseEvent(event)

    def setSelected(self, item):
        if self._selected == item:
            return
        if self._selected:
            try:
                self._selected.unselect()
            except AttributeError:
                pass
        self._selected = item
        if item:
            try:
                item.select()
                self.reinitSelectedProperties()
            except AttributeError:
                self.parent().propertiesEditor.setNoItem()
        else:
            self.parent().propertiesEditor.setNoItem()

    def reinitSelectedProperties(self):
        if self._selected:
            if isinstance(self._selected, ArcItem):
                self.parent().propertiesEditor.setArcItem().setSelectedArc(self._selected)
            elif isinstance(self._selected, NodeItem):
                self.parent().propertiesEditor.setNodeItem().setSelectedNode(self._selected)
            elif isinstance(self._selected, ConnectedComponent):
                self.parent().propertiesEditor.setConnectedComponentItem().setSelectedConnectedComponent(self._selected)
        else:
            self.parent().propertiesEditor.setNoItem()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_N:
            self.setNodeMode()
        elif event.key() == QtCore.Qt.Key_A:
            if self.isPathMode():
                self.setStarMode()
            elif self.isStarMode():
                self.setSeparateInputMode()
            elif self.isSeparateInputMode():
                self.setSeparateOutputMode()
            else:
                self.setPathMode()
        elif event.key() == QtCore.Qt.Key_S:
            self.setSelectMode()
        elif event.key() == QtCore.Qt.Key_C:
            self.setComponentMode()
        elif event.key() == QtCore.Qt.Key_Delete:
            if self.isComponentMode() and self._selected is not None:
                self._selected.remove()
            elif self._selected:
                self.deleteSelected()
        else:
            item = self.mouseGrabberItem()
            try:
                item.keyReleaseEvent(event)
            except AttributeError:
                pass

    def setNodeMode(self):
        self.modeController.setNodeMode()
        if isinstance(self._selected, ArcItem) or isinstance(self._selected, ConnectedComponent):
            self.setSelected(None)

    def setPathMode(self):
        self.modeController.setPathMode()
        if isinstance(self._selected, ConnectedComponent):
            self.setSelected(None)

    def setStarMode(self):
        self.modeController.setStarMode()
        if isinstance(self._selected, ConnectedComponent):
            self.setSelected(None)

    def setSelectMode(self):
        self.modeController.setSelectMode()
        self.setSelected(None)

    def setComponentMode(self):
        self.modeController.setComponentMode()
        self.setSelected(None)

    def setSeparateInputMode(self):
        self.modeController.setSeparateInputMode()
        self.setSelected(None)

    def setSeparateOutputMode(self):
        self.modeController.setSeparateOutputMode()
        self.setSelected(None)

    def isNodeMode(self):
        return self.modeController.isNodeMode()

    def isArcMode(self):
        return self.modeController.isArcMode()

    def isPathMode(self):
        return self.modeController.isPathMode()

    def isStarMode(self):
        return self.modeController.isStarMode()

    def isSelectMode(self):
        return self.modeController.isSelectMode()

    def isComponentMode(self):
        return self.modeController.isComponentMode()

    def isSeparateInputMode(self):
        return self.modeController.isSeparateInputMode()

    def isSeparateOutputMode(self):
        return self.modeController.isSeparateOutputMode()

    def deleteSelected(self):
        self.mainWindow.stack.push(DeleteItemCommand(self, self._selected))
        self.setSelected(None)

    def deleteItem(self, item):
        item.remove()
        self.removeItem(item)


class NodesIdsGenerator():
    def __init__(self):
        self.reinit()

    def reinit(self):
        self._nodeId = 0
        self._nextIds = deque([0])

    def getNodeId(self):
        return self._nodeId

    def getNextIds(self):
        return self._nextIds

    def setNodeId(self, nodeId):
        self._nodeId = nodeId

    def setNextIds(self, nextIds):
        self._nextIds = nextIds

    def getNextNodeId(self):
        num = self._nextIds.popleft()
        if len(self._nextIds) == 0:
            self._nodeId += 1
            self._nextIds.append(self._nodeId)
        return num

    def removeNodeIndex(self, index):
        self._nextIds.appendleft(index)


class ModeController():
    NodeMode = 0
    PathMode = 1
    StarMode = 2
    SelectMode = 3
    ComponentMode = 4
    SeparateInputMode = 5
    SeparateOutputMode = 6

    def __init__(self, mainWindow=None):
        self._mode = ModeController.NodeMode
        self.mainWindow = mainWindow

    def setNodeMode(self):
        self.setMode(ModeController.NodeMode)
        self.mainWindow.statusBar().showMessage('Node mode')

    def setPathMode(self):
        self.setMode(ModeController.PathMode)
        self.mainWindow.statusBar().showMessage('Path mode')

    def setStarMode(self):
        self.setMode(ModeController.StarMode)
        self.mainWindow.statusBar().showMessage('Star mode')

    def setSelectMode(self):
        self.setMode(ModeController.SelectMode)
        self.mainWindow.statusBar().showMessage('Select mode')

    def setComponentMode(self):
        self.setMode(ModeController.ComponentMode)
        self.mainWindow.statusBar().showMessage('Component mode')

    def setSeparateInputMode(self):
        self.setMode(ModeController.SeparateInputMode)
        self.mainWindow.statusBar().showMessage('Separate input mode')

    def setSeparateOutputMode(self):
        self.setMode(ModeController.SeparateOutputMode)
        self.mainWindow.statusBar().showMessage('Separate output mode')

    def setMode(self, mode):
        self._mode = mode

    def isNodeMode(self):
        return self._mode == ModeController.NodeMode

    def isArcMode(self):
        return self.isPathMode() or self.isStarMode()

    def isPathMode(self):
        return self._mode == ModeController.PathMode

    def isStarMode(self):
        return self._mode == ModeController.StarMode

    def isSeparateInputMode(self):
        return self._mode == ModeController.SeparateInputMode

    def isSeparateOutputMode(self):
        return self._mode == ModeController.SeparateOutputMode

    def isSelectMode(self):
        return self._mode == ModeController.SelectMode

    def isComponentMode(self):
        return self._mode == ModeController.ComponentMode