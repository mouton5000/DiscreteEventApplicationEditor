__author__ = 'mouton'


from PyQt4 import QtCore
from PyQt4.QtGui import QGraphicsEllipseItem, QBrush
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
        self._center = vector(x, y)
        self.outputArcs = []
        self.inputArcs = []

        self._isMoving = False
        self._moveFrom = None

        self._label = ''
        self._tokens = []

        self.scene().parent().window().stack.push(AddItemCommand(self.scene(), self))

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

    # def mouseDoubleClickEvent(self, QGraphicsSceneMouseEvent):
    #     if self.scene().isNodeMode():
    #         self.scene().parent().window().stack.push(SetActiveNodeCommand(self, not self._isActive))

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.scene().parent().window().stack.push(MoveNodeCommand(self, self._moveFrom, self._center))
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

    def getTokensStr(self):
        return '\n'.join(self._tokens)

    def setTokens(self, tokens):
        try:
            if tokens == '':
                self._tokens = []
            else:
                self._tokens = tokens.split('\n')  # consequences is a string
        except AttributeError:
            self._tokens = tokens  # consequences is a list

    def mouseMoveEvent(self, event):
        if not self.scene().isNodeMode():
            return

        if not self._isMoving:
            self._isMoving = True
            self._moveFrom = self._center

        x = event.scenePos().x()
        y = event.scenePos().y()
        self.setXY(x, y)

    def setXY(self, x, y):
        dx, dy = x - self._center.x, y - self._center.y
        self.moveBy(dx, dy)
        self._center = vector(x, y)

        for a in self.inputArcs:
            a.drawPath()

        for a in self.outputArcs:
            a.drawPath()

        self._labelItem.setCenter(self._center)

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
            self.scene().parent().window().stack.push(DeleteItemCommand(self.scene(), a))
        for a in copy(self.outputArcs):
            self.scene().parent().window().stack.push(DeleteItemCommand(self.scene(), a))
        self.scene().removeItem(self._labelItem)

    def __str__(self):
        return str(self._num)

    def __repr__(self):
        return str(self._num)