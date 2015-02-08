from copy import copy
import itertools
from gui.LabelItems import LabelItem

__author__ = 'mouton'


from PyQt4 import QtCore
from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsView, QGraphicsScene
from undoRedoActions import *
from NodeItems import NodeItem, ConnectedComponent
from ArcItems import ArcItem
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

    def clear(self):
        super(SceneWidget, self).clear()
        self.init()

    def getNextNodeId(self):
        return self.nodesIdsGenerator.getNextNodeId()

    def removeNodeIndex(self, index):
        self.nodesIdsGenerator.removeNodeIndex(index)

    def addNode(self, x, y):
        nodeItem = NodeItem(x, y, scene=self)
        return self.addNodeItem(nodeItem)

    def addNodeItem(self, nodeItem):
        self.mainWindow.stack.push(AddNodeItemCommand(self, nodeItem))
        return nodeItem

    def addNodeWithoutStack(self, nodeItem):
        # Should not be called by any instance but a QUndoRedoCommand instance
        num = self.getNextNodeId()
        nodeItem.num = num
        self.nodes.append(nodeItem)
        if nodeItem not in self.items():
            self.addItem(nodeItem)
        self.setSelected(nodeItem)
        labelItem = nodeItem.getLabelItem()
        if labelItem not in self.items():
            self.addItem(labelItem)
        self.parent().showTab()
        return nodeItem

    def removeNode(self, nodeItem):
        self.mainWindow.stack.push(RemoveNodeItemCommand(self, nodeItem))

    def removeNodeWithoutStack(self, nodeItem, arcs):
        # Should not be called by any instance but a QUndoRedoCommand instance
        self.nodes.remove(nodeItem)
        self.removeNodeIndex(nodeItem.num)
        for a in arcs:
            self.removeArcWithoutStack(a)

        self.removeItem(nodeItem.getLabelItem())
        self.removeItem(nodeItem)
        self.parent().showTab()

    def undoRemoveNodeWithoutStack(self, nodeItem, arcs):
        self.addNodeWithoutStack(nodeItem)
        for arc in arcs:
            self.addArcWithoutStack(arc)
        self.setSelected(nodeItem)

    def getCloseNodeOf(self, x, y):
        for node in self.nodes:
            if node.isCloseTo(x, y):
                return node

    def addArc(self, n1, n2):
        arcItem = ArcItem(n1, n2, scene=self)
        self.mainWindow.stack.push(AddArcItemCommand(self, arcItem))
        if self.isPathMode():
            self.setSelected(n2)
        elif self.isStarMode():
            self.setSelected(n1)
        return arcItem

    def addArcWithoutStack(self, arcItem):
        # Should not be called by any instance but a QUndoRedoCommand instance
        if arcItem not in self.items():
            self.addItem(arcItem)
        arcItem.node1.outputArcs.append(arcItem)
        arcItem.node2.inputArcs.append(arcItem)
        self.setSelected(arcItem)
        labelItem = arcItem.getLabelItem()
        if labelItem not in self.items():
            self.addItem(labelItem)
        self.parent().showTab()
        arcItem.drawPath()

    def removeArc(self, arcItem):
        self.mainWindow.stack.push(RemoveArcItemCommand(self, arcItem))

    def removeArcWithoutStack(self, arcItem):
        # Should not be called by any instance but a QUndoRedoCommand instance
        arcItem.node1.outputArcs.remove(arcItem)
        arcItem.node1.reorganizeArcLabels()
        arcItem.node2.inputArcs.remove(arcItem)
        self.removeItem(arcItem.getLabelItem())
        self.removeItem(arcItem)
        self.parent().showTab()

    def removeConnectedComponent(self, connectedComponent):
        for node in connectedComponent.nodes:
            self.removeNode(node)

    def changeConnectedComponentSceneByIndex(self, connectedComponent, newSceneIndex):
        if newSceneIndex == -1:
            return
        scenes = self.parent().mainWindow.scenes()
        newScene = next(itertools.islice(scenes, newSceneIndex, newSceneIndex + 1))
        if self == newScene:
            return
        self.changeConnectedComponentScene(connectedComponent, newScene)

    def changeConnectedComponentScene(self, connectedComponent, newScene):
        self.mainWindow.stack.push(ChangeConnectedComponentSceneCommand(self, connectedComponent, newScene))

    def changeConnectedComponentSceneWithoutStack(self, connectedComponent, newScene):
        connectedComponent.setScene(newScene)
        for node in connectedComponent.nodes:
            self.nodes.remove(node)
            self.removeItem(node.getLabelItem())
            newScene.nodes.append(node)
            newScene.addItem(node)
            newScene.addItem(node.getLabelItem())
            for a in node.outputArcs:
                self.removeItem(a)
                self.removeItem(a.getLabelItem())
                newScene.addItem(a)
                newScene.addItem(a.getLabelItem())
        self.setSelected(None)
        newScene.parent().showTab()
        newScene.setComponentMode()
        newScene.setSelected(connectedComponent)

    def mergeNodes(self, fromNode, toNode):
        self.mainWindow.stack.push(MergeNodesCommand(self, fromNode, toNode))

    def mergeNodesWithoutStack(self, fromNode, toNode, inputArcsOfFromNode, outputArcsOfFromNode):
        for arc in inputArcsOfFromNode:
            arc.changeOutputWithoutStack(toNode)
        for arc in outputArcsOfFromNode:
            arc.changeInputWithoutStack(toNode)
        self.removeNodeWithoutStack(fromNode)
        self.setSelected(toNode)
        self.parent().showTab()

    def unmergeNodesWithoutStack(self, fromNode, inputArcsOfFromNode, outputArcsOfFromNode):
        self.addNodeWithoutStack(fromNode)
        for arc in inputArcsOfFromNode:
            arc.changeOutputWithoutStack(fromNode)
        for arc in outputArcsOfFromNode:
            arc.changeInputWithoutStack(fromNode)
        self.setSelected(fromNode)
        self.parent().showTab()

    def setSelected(self, item):
        if self._selected == item:
            return
        if self._selected is not None:
            try:
                self._selected.unselect()
            except AttributeError:
                pass
        self._selected = item
        if item is not None:
            try:
                item.select()
                self.reinitSelectedProperties()
            except AttributeError:
                self.parent().propertiesEditor.setNoItem()
        else:
            self.parent().propertiesEditor.setNoItem()

    def deleteSelected(self):
        if self._selected is None:
            return
        if isinstance(self._selected, NodeItem):
            self.removeNode(self._selected)
        elif isinstance(self._selected, ArcItem):
            self.removeArc(self._selected)
        elif isinstance(self._selected, ConnectedComponent):
            self.removeConnectedComponent(self._selected)
        self.setSelected(None)

    def reinitSelectedProperties(self):
        if self._selected is not None:
            if isinstance(self._selected, ArcItem):
                self.parent().propertiesEditor.setArcItem().setSelectedArc(self._selected)
            elif isinstance(self._selected, NodeItem):
                self.parent().propertiesEditor.setNodeItem().setSelectedNode(self._selected)
            elif isinstance(self._selected, ConnectedComponent):
                self.parent().propertiesEditor.setConnectedComponentItem().setSelectedConnectedComponent(self._selected)
        else:
            self.parent().propertiesEditor.setNoItem()

    def mousePressEvent(self, event):
        super(SceneWidget, self).mousePressEvent(event)
        item = self.mouseGrabberItem()
        if self.isComponentMode():
            # selected is a connected component if exists
            if item is not None and self._selected is not None and item in self._selected:
                self._selected.initMove()

    def mouseMoveEvent(self, event):
        item = self.mouseGrabberItem()
        if self.isComponentMode():
            # selected is a connected component if exists
            if item is not None and self._selected is not None and item in self._selected:
                x, y = event.scenePos().x(), event.scenePos().y()
                self._selected.move(x, y)
        else:
            super(SceneWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        mouseGrabberItem = self.mouseGrabberItem()
        if self.isNodeMode():
            self.mouseReleaseEventNodeMode(event, mouseGrabberItem)
        elif self.isMergeNodeMode():
            self.mouseReleaseEventMergeNodeMode(event, mouseGrabberItem)
        elif self.isArcMode():
            self.mouseReleaseEventArcMode(event, mouseGrabberItem)
        elif self.isSeparateInputMode() or self.isSeparateOutputMode():
            self.mouseReleaseEventSeparateMode(event, mouseGrabberItem)
        elif self.isSelectMode():
            self.mouseReleaseEventSelectMode(event, mouseGrabberItem)
        elif self.isComponentMode():
            self.mouseReleaseEventConnectedComponentMode(event, mouseGrabberItem)

    def mouseReleaseEventNodeMode(self, event, mouseGrabberItem):
        if mouseGrabberItem is None:
            x, y = event.scenePos().x(), event.scenePos().y()
            self.addNode(x, y)
        elif isinstance(mouseGrabberItem, NodeItem):
            self.setSelected(mouseGrabberItem)
            mouseGrabberItem.mouseReleaseEvent(event)
        elif isinstance(mouseGrabberItem, LabelItem):
            self.setSelected(mouseGrabberItem.attachedItem())
            mouseGrabberItem.mouseReleaseEvent(event)
        else:
            mouseGrabberItem.mouseReleaseEvent(event)

    def mouseReleaseEventMergeNodeMode(self, event, mouseGrabberItem):
        if mouseGrabberItem is None or not isinstance(mouseGrabberItem, NodeItem):
            self.setSelected(None)
        else:
            if self._selected is not None and self._selected != mouseGrabberItem:
                self.mergeNodes(self._selected, mouseGrabberItem)
            else:
                self.setSelected(mouseGrabberItem)
            mouseGrabberItem.mouseReleaseEvent(event)

    def mouseReleaseEventArcMode(self, event, mouseGrabberItem):
        if mouseGrabberItem is None:
                self.setSelected(None)
        else:
            if isinstance(mouseGrabberItem, NodeItem):
                if isinstance(self._selected, NodeItem):
                    self.addArc(self._selected, mouseGrabberItem)
                else:
                    self.setSelected(mouseGrabberItem)
            elif isinstance(mouseGrabberItem, ArcItem):
                self.setSelected(mouseGrabberItem)
            elif isinstance(mouseGrabberItem, LabelItem):
                self.setSelected(mouseGrabberItem.attachedItem())
            mouseGrabberItem.mouseReleaseEvent(event)

    def mouseReleaseEventSeparateMode(self, event, mouseGrabberItem):
        if mouseGrabberItem is None:
            self.setSelected(None)
        elif isinstance(mouseGrabberItem, ArcItem):
            mouseGrabberItem.mouseReleaseEvent(event)
            self.setSelected(mouseGrabberItem)
        else:
            mouseGrabberItem.mouseReleaseEvent(event)

    def mouseReleaseEventSelectMode(self, event, mouseGrabberItem):
        if mouseGrabberItem is not None:
            if not isinstance(mouseGrabberItem, LabelItem):
                self.setSelected(mouseGrabberItem)
            else:
                self.setSelected(mouseGrabberItem.attachedItem())
            mouseGrabberItem.mouseReleaseEvent(event)

    def mouseReleaseEventConnectedComponentMode(self, event, mouseGrabberItem):

        def _selectConnectedComponent():
            try:
                self.setSelected(mouseGrabberItem.getConnectedComponent())
            except AttributeError:
                pass

        if self._selected is not None:
            # selected is a connected component
            self._selected.endMove()
            if mouseGrabberItem is not None:
                if mouseGrabberItem not in self._selected:
                    _selectConnectedComponent()
                mouseGrabberItem.mouseReleaseEvent(event)
            else:
                self.setSelected(None)
        else:
            if mouseGrabberItem is not None:
                _selectConnectedComponent()
                mouseGrabberItem.mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_N and event.modifiers() == QtCore.Qt.ShiftModifier:
            self.setMergeNodeMode()
        elif event.key() == QtCore.Qt.Key_N:
            self.setNodeMode()
        elif event.key() == QtCore.Qt.Key_A and event.modifiers() == QtCore.Qt.ShiftModifier:
            if self.isSeparateInputMode():
                self.setSeparateOutputMode()
            else:
                self.setSeparateInputMode()
        elif event.key() == QtCore.Qt.Key_A:
            if self.isPathMode():
                self.setStarMode()
            else:
                self.setPathMode()
        elif event.key() == QtCore.Qt.Key_S:
            self.setSelectMode()
        elif event.key() == QtCore.Qt.Key_C:
            self.setComponentMode()
        elif event.key() == QtCore.Qt.Key_Delete:
            self.deleteSelected()
        else:
            item = self.mouseGrabberItem()
            try:
                item.keyReleaseEvent(event)
            except AttributeError:
                pass

    def setNodeMode(self):
        self.modeController.setNodeMode()
        if not isinstance(self._selected, NodeItem):
            self.setSelected(None)

    def setMergeNodeMode(self):
        self.modeController.setMergeNodeMode()
        if not isinstance(self._selected, NodeItem):
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

    def isMergeNodeMode(self):
        return self.modeController.isMergeNodeMode()

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
    MergeNodeMode = 7

    def __init__(self, mainWindow=None):
        self._mode = ModeController.NodeMode
        self.mainWindow = mainWindow

    def setNodeMode(self):
        self.setMode(ModeController.NodeMode)
        self.mainWindow.statusBar().showMessage('Node mode')

    def setMergeNodeMode(self):
        self.setMode(ModeController.MergeNodeMode)
        self.mainWindow.statusBar().showMessage('Merge node mode')

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

    def isMergeNodeMode(self):
        return self._mode == ModeController.MergeNodeMode

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