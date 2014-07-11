__author__ = 'mouton'


from PyQt4 import QtCore
from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsView, QGraphicsScene
from undoRedoActions import *
from NodeItems import NodeItem
from ArcItems import ArcItem, CycleArcItem
from collections import deque


class ViewWidget(QGraphicsView):
    def __init__(self, parent=None, mainWindow=None):
        super(ViewWidget, self).__init__(parent)
        self.mainWindow = mainWindow
        scene = SceneWidget(self, mainWindow=self.mainWindow)
        self.setScene(scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rect = QRectF(-200, -200, 400, 400)
        self.setSceneRect(self.rect)
        self.px = None
        self.py = None
        self.propertiesEditor = None
        self.scl = 1

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
        else:
            super(ViewWidget, self).keyPressEvent(event)
        if dx != 0 or dy != 0:
            self.translate(dx, dy)

    def translate(self, dx, dy):
        self.rect.translate(-dx, -dy)
        self.setSceneRect(self.rect)

    def setPropertiesEditor(self, pe):
        self.propertiesEditor = pe


class SceneWidget(QGraphicsScene):
    NodeMode = 0
    PathMode = 1
    StarMode = 2
    SelectMode = 3

    def __init__(self, parent=None, mainWindow=None):
        super(SceneWidget, self).__init__(parent)
        self.mainWindow = mainWindow
        self.init()

    def init(self):
        self.nodes = []
        self._nodeId = 0
        self._nextIds = deque([0])
        self._selected = None
        self._mode = None
        self.setNodeMode()

    def getNodeId(self):
        return self._nodeId

    def getNextIds(self):
        return self._nextIds

    def setNodeId(self, nodeId):
        self._nodeId = nodeId

    def setNextIds(self, nextIds):
        self._nextIds = nextIds

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
        num = self._nextIds.popleft()
        if len(self._nextIds) == 0:
            self._nodeId += 1
            self._nextIds.append(self._nodeId)
        return num

    def removeNodeIndex(self, index):
        self._nextIds.appendleft(index)

    def addNode(self, x, y):
        num = self.getNextNodeId()
        node = NodeItem(x, y, num, scene=self)
        self.setSelected(node)
        # Apparently, addItem is not called when an item is created
        node.add()
        return node

    def addArc(self, n1, n2):
        if n1 == n2:
            arc = CycleArcItem(n1, scene=self)
        else:
            arc = ArcItem(n1, n2, scene=self)
        if self.isPathMode():
            self.setSelected(n2)
        return arc

    def mouseReleaseEvent(self, event):
        item = self.mouseGrabberItem()
        if self.isNodeMode():
            if not item:
                x, y = event.scenePos().x(), event.scenePos().y()
                self.addNode(x, y)
            elif isinstance(item, NodeItem):
                self.setSelected(item)
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
                else:
                    self.setSelected(item)
                item.mouseReleaseEvent(event)
        elif self.isSelectMode():
            if item:
                self.setSelected(item)
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
                if isinstance(item, ArcItem):
                    self.parent().propertiesEditor.setArcItem().setSelectedArc(item)
                elif isinstance(item, NodeItem):
                    self.parent().propertiesEditor.setNodeItem().setSelectedNode(item)
            except AttributeError:
                self.parent().propertiesEditor.setNoItem()
        else:
            self.parent().propertiesEditor.setNoItem()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_N:
            self.setNodeMode()
        elif event.key() == QtCore.Qt.Key_A:
            if not self.isPathMode():
                self.setPathMode()
            else:
                self.setStarMode()
        elif event.key() == QtCore.Qt.Key_S:
            self.setSelectMode()
        elif event.key() == QtCore.Qt.Key_Delete:
            if self._selected:
                self.deleteSelected()
        else:
            item = self.mouseGrabberItem()
            try:
                item.keyReleaseEvent(event)
            except AttributeError:
                pass

    def setNodeMode(self):
        self.setMode(SceneWidget.NodeMode)
        self.mainWindow.statusBar().showMessage('Node mode')
        if isinstance(self._selected, ArcItem):
            self.setSelected(None)

    def setPathMode(self):
        self.setMode(SceneWidget.PathMode)
        self.mainWindow.statusBar().showMessage('Path mode')

    def setStarMode(self):
        self.setMode(SceneWidget.StarMode)
        self.mainWindow.statusBar().showMessage('Star mode')

    def setSelectMode(self):
        self.setMode(SceneWidget.SelectMode)
        self.mainWindow.statusBar().showMessage('Select mode')

    def setMode(self, mode):
        self._mode = mode

    def isNodeMode(self):
        return self._mode == SceneWidget.NodeMode

    def isArcMode(self):
        return self.isPathMode() or self.isStarMode()

    def isPathMode(self):
        return self._mode == SceneWidget.PathMode

    def isStarMode(self):
        return self._mode == SceneWidget.StarMode

    def isSelectMode(self):
        return self._mode == SceneWidget.SelectMode

    def deleteSelected(self):
        self.parent().window().stack.push(DeleteItemCommand(self, self._selected))
        self.setSelected(None)

    def deleteItem(self, item):
        item.remove()
        self.removeItem(item)