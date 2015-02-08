import itertools

__author__ = 'mouton'


from PyQt4 import QtCore
from PyQt4.QtGui import QGraphicsEllipseItem, QBrush
from visual import vector
from copy import copy
from undoRedoActions import *
from gui.LabelItems import LabelItem


class NodeItem(QGraphicsEllipseItem):
    NodeWidth = 20

    def __init__(self, x, y, parent=None, scene=None):
        super(NodeItem, self).__init__(x - NodeItem.NodeWidth, y - NodeItem.NodeWidth, NodeItem.NodeWidth * 2,
                                       NodeItem.NodeWidth * 2, parent, scene)

        self._num = None
        self.outputArcs = []
        self.inputArcs = []
        self._label = ''
        self._tokens = []

        self._center = vector(x, y)
        self._isMoving = False
        self._moveFrom = None

        self.setBrush(QBrush(QtCore.Qt.black))

        self._labelItem = None

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    def getLabelItem(self):
        if self._labelItem is None:
            self.setLabelItem(LabelItem(scene=self.scene()))
        return self._labelItem

    def setLabelItem(self, labelItem):
        self._labelItem = labelItem
        self._labelItem.setText(str(self.num))
        self._labelItem.setBrush(QBrush(QtCore.Qt.black))
        self._labelItem.setCenter(self.getXY())
        self._labelItem.setOffset(vector(0, NodeItem.NodeWidth * 2))
        labelItem.setAttachedItem(self)

    def reorganizeArcLabels(self):
        for j, arc in enumerate(self.outputArcs):
            arc.setLabelItemText(j, arc.getLabel())

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.commitMove()
            self._moveFromX = None
            self._moveFromY = None
            self._isMoving = False
        self.ungrabMouse()

    def commitMove(self):
        self.scene().mainWindow.stack.push(MoveNodeCommand(self.scene(), self, self._moveFrom, self._center))

    def moveWithoutStack(self, center):
        self.setXY(center.x, center.y)
        self.scene().parent().showTab()

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
        if self.scene().isNodeMode() or self.scene().isMergeNodeMode():
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

    def isCloseTo(self, x, y):
        return (self._center - vector(x, y)).mag < NodeItem.NodeWidth

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

    def getConnectedComponent(self):
        coComp = ConnectedComponent(self.scene(), self)
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

    def __init__(self, scene, node):
        self.nodes = set([])
        self.arcs = set([])
        self.px = None
        self.py = None

        self.firstNode = node

        self._x = 0
        self._y = 0

        self._isMoving = False
        self._moveFrom = None
        self._scene = scene

    def scene(self):
        return self._scene

    def setScene(self, scene):
        self._scene = scene

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

    def initMove(self):
        self._moveFrom = vector(self._x, self._y)
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
        self._x += dx
        self._y += dy

    def endMove(self):
        if self._isMoving:
            self.commitMove()
            self._isMoving = False
        else:
            self._moveFrom = None

    def commitMove(self):
        self.scene().mainWindow.stack.push(
            MoveConnectedComponentCommand(self.scene(), self, self._moveFrom, vector(self._x, self._y)))

    def moveWithoutStack(self, center):
        dx, dy = center.x - self._x, center.y - self._y
        self.setDXDY(dx, dy)
        self.scene().parent().showTab()

    def __str__(self):
        return str(self.nodes) + ' ' + str(self.arcs)

    def __repr__(self):
        return str(self.nodes) + ' ' + str(self.arcs)