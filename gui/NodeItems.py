import itertools

__author__ = 'mouton'


from PyQt4 import QtCore
from PyQt4.QtGui import QGraphicsEllipseItem, QBrush
from PyQt4.QtCore import pyqtSlot
from visual import vector
from copy import copy
from undoRedoActions import *
from gui.LabelItems import LabelItem


class NodeItem(QGraphicsEllipseItem):
    NodeWidth = 20

    def __init__(self, x, y, num, parent=None, scene=None):
        super(NodeItem, self).__init__(x - NodeItem.NodeWidth, y - NodeItem.NodeWidth, NodeItem.NodeWidth * 2,
                                       NodeItem.NodeWidth * 2, parent, scene)

        self._num = num
        self.outputArcs = []
        self.inputArcs = []
        self._label = ''
        self._tokens = []

        self._center = vector(x, y)
        self._isMoving = False
        self._moveFrom = None

        self.scene().mainWindow.stack.push(AddItemCommand(self.scene(), self))

        self.setBrush(QBrush(QtCore.Qt.black))

        self._labelItem = LabelItem(str(self.num),
                                       scene=self.scene())
        self._labelItem.setBrush(QBrush(QtCore.Qt.black))
        self._labelItem.setCenter(self._center)
        self._labelItem.setOffset(vector(0, NodeItem.NodeWidth * 2))

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    def add(self):
        self.scene().nodes.append(self)

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.scene().mainWindow.stack.push(MoveNodeCommand(self.scene(), self, self._moveFrom, self._center))
            self._moveFromX = None
            self._moveFromY = None
            self._isMoving = False
        self.ungrabMouse()

    def select(self):
        br = self.brush()
        br.setStyle(QtCore.Qt.Dense3Pattern)
        self.setBrush(br)

    def unselect(self):
        br = self.brush()
        br.setStyle(QtCore.Qt.SolidPattern)
        self.setBrush(br)

    # def setActive(self, isActive):
    #     self._isActive = isActive
    #     br = self.brush()
    #     if isActive:
    #         br.setColor(QtCore.Qt.red)
    #     else:
    #         br.setColor(QtCore.Qt.black)
    #     self.setBrush(br)

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label
        if label:
            self._labelItem.setText(str(self.num) + ' : ' + label)
        else:
            self._labelItem.setText(str(self.num))

    def getLabelItem(self):
        return self._labelItem

    def getTokens(self):
        return self._tokens

    def setTokens(self, tokens):
        self._tokens = tokens

    def setToken(self, index, text):
        self._tokens[index] = str(text)

    def addToken(self):
        self._tokens.append('')

    def removeToken(self, index):
        self._tokens.pop(index)

    def mouseMoveEvent(self, event):
        if self.scene().isNodeMode():
            if not self._isMoving:
                self._isMoving = True
                self._moveFrom = self._center

            x = event.scenePos().x()
            y = event.scenePos().y()
            self.setXY(x, y)
        elif self.scene().isComponentMode():
            pass
            # self.scene().getSelected()

    def setDXDY(self, dx, dy, drawArcs=True):
        self.moveBy(dx, dy)
        x, y = dx + self._center.x, dy + self._center.y
        self._center = vector(x, y)

        if drawArcs:
            for a in self.inputArcs:
                a.drawPath()

            for a in self.outputArcs:
                a.drawPath()

        self._labelItem.setCenter(self._center)

    def setXY(self, x, y):
        dx, dy = x - self._center.x, y - self._center.y
        self.setDXDY(dx, dy)

    def getXY(self):
        return self._center

    def isPredecessorOf(self, node):
        for a in self.outputArcs:
            if a.node2 == node:
                return True
        return False

    def isSuccessorOf(self, node):
        for a in self.inputArcs:
            if a.node1 == node:
                return True
        return False

    def remove(self):
        self.scene().nodes.remove(self)
        self.scene().removeNodeIndex(self.num)

        for a in copy(self.inputArcs):
            self.scene().mainWindow.stack.push(DeleteItemCommand(self.scene(), a))
        for a in copy(self.outputArcs):
            self.scene().mainWindow.stack.push(DeleteItemCommand(self.scene(), a))

        self.scene().removeItem(self._labelItem)

    def getConnectedComponent(self):
        coComp = ConnectedComponent(self.scene())
        toVisit = set([self])
        while len(toVisit) != 0:
            node = toVisit.pop()
            coComp.addNode(node)
            node.connectedComponent = coComp
            for a in node.inputArcs:
                if a not in coComp:
                    coComp.addArc(a)
                    toVisit.add(a.node1)
            for a in node.outputArcs:
                if a not in coComp:
                    coComp.addArc(a)
                    toVisit.add(a.node2)
        return coComp

    def __str__(self):
        return str(self._num)

    def __repr__(self):
        return str(self._num)


class ConnectedComponent():

    def __init__(self, scene):
        self.nodes = set([])
        self.arcs = set([])
        self.px = None
        self.py = None

        self._isMoving = False
        self._moveFrom = None
        self._scene = scene

    def scene(self):
        return self._scene

    def setScene(self, sceneIndex):
        if sceneIndex == -1:
            return
        oldScene = self._scene
        scenes = oldScene.parent().mainWindow.scenes()
        print sceneIndex
        newScene = next(itertools.islice(scenes, sceneIndex, sceneIndex + 1))
        if oldScene == newScene:
            return

        self.scene().mainWindow.stack.push(ChangeConnectedComponentSceneCommand(
            oldScene, self, newScene))



    def addNode(self, node):
        self.nodes.add(node)

    def addArc(self, arc):
        self.arcs.add(arc)

    def __contains__(self, elem):
        return elem in self.nodes or elem in self.arcs

    def select(self):
        for node in self.nodes:
            node.select()
        for arc in self.arcs:
            arc.select()

    def unselect(self):
        for node in self.nodes:
            node.unselect()
        for arc in self.arcs:
            arc.unselect()

    def initMove(self, x, y):
        self._moveFrom = vector(x, y)
        self.px = None
        self.py = None

    def move(self, x, y):
        if not self._isMoving:
            self._isMoving = True

        if self.px:
            dx, dy = x - self.px, y - self.py
            self.setDXDY(dx, dy)

        self.px = x
        self.py = y

    def setDXDY(self, dx, dy):
        for node in self.nodes:
            node.setDXDY(dx, dy, False)
        for arc in self.arcs:
            arc.drawPath()

    def endMove(self, x, y):
        if self._isMoving:
            self.scene().mainWindow.stack.push(MoveConnectedComponentCommand(self.scene(), self, self._moveFrom,
                                                                                    vector(x, y)))
            self._isMoving = False
        else:
            self._moveFrom = None

    def remove(self):
        for node in self.nodes:
            self.scene().mainWindow.stack.push(DeleteItemCommand(self.scene(), node))
        self.scene().setSelected(None)

    def moveToNextScene(self):
        scene = self.scene()
        scene2 = scene.parent().parent().parent().getScene(2)
        for node in self.nodes:
            scene.removeItem(node)
            scene2.addItem(node)
            scene.removeItem(node._labelItem)
            scene2.addItem(node._labelItem)
        for arc in self.arcs:
            scene.removeItem(arc)
            scene2.addItem(arc)
            scene.removeItem(arc._labelItem)
            scene2.addItem(arc._labelItem)
        self._scene = scene

    def __str__(self):
        return str(self.nodes) + ' ' + str(self.arcs)

    def __repr__(self):
        return str(self.nodes) + ' ' + str(self.arcs)