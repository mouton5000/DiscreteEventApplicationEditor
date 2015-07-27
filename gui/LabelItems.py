from PyQt4.QtCore import QPointF
from PyQt4.QtGui import QGraphicsSimpleTextItem
from euclid import Vector2
from undoRedoActions import MoveNodeLabelItemCommand, MoveArcLabelItemCommand
from math import pi, cos, copysign
from gui.EditorItem import NODE_GRID

class LabelItem(QGraphicsSimpleTextItem):
    def __init__(self, parent=None, scene=None):
        super(LabelItem, self).__init__('', parent, scene)
        self._isMoving = False
        self._center = Vector2(0, 0)

        self._linkToParentItem = self.scene().addLine(0, 0, 0, 0)
        self._linkToParentItem.setVisible(False)

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.commitMove()
            self._isMoving = False
            self._linkToParentItem.setVisible(False)
        self.ungrabMouse()

    def setAttachedItem(self, attachedItem):
        self._attachedItem = attachedItem

    def attachedItem(self):
        return self._attachedItem

    def setCenter(self, center):
        self._center = center
        line = self._linkToParentItem.line()
        line.setP1(QPointF(center.x, center.y))
        self._linkToParentItem.setLine(line)
        self.updatePos()


class NodeLabelItem(LabelItem):
    def __init__(self, parent=None, scene=None):
        super(NodeLabelItem, self).__init__(parent=parent, scene=scene)
        self._offset = Vector2(0, 0)
        self._moveFromOffset = False

    def moveWithoutStack(self, offset):
        self.setOffset(offset)
        self.scene().parent().showTab()

    def mouseMoveEvent(self, event):
        if not self._isMoving:
            self._isMoving = True
            self._moveFromOffset = self._offset
            self._linkToParentItem.setVisible(True)

        x = NODE_GRID(event.scenePos().x())
        y = NODE_GRID(event.scenePos().y())
        epos = Vector2(x, y)
        self.setOffset(epos - self._center)

    def commitMove(self):
        self.scene().mainWindow.stack.push(
            MoveNodeLabelItemCommand(self.scene(), self, self._moveFromOffset, self._offset))

    def setOffset(self, offset):
        dpos = offset - self._offset
        self.moveBy(dpos.x, dpos.y)
        self._offset = offset
        self.updatePos()

        rect = self.boundingRect()
        line = self._linkToParentItem.line()
        line.setP2(QPointF(self.pos().x() + rect.width() / 2, self.pos().y() + rect.height()))
        self._linkToParentItem.setLine(line)

    def getOffset(self):
        return self._offset

    def updatePos(self):
        rect = self.boundingRect()
        pos = self._center + self._offset
        self.setPos(pos.x - rect.width() / 2, pos.y - rect.height() / 2)


class ArcLabelItem(LabelItem):
    def __init__(self, parent=None, scene=None):
        super(ArcLabelItem, self).__init__(parent=parent, scene=scene)
        self._angle = pi / 2
        self._ratio = 0.1
        self._arcVector = Vector2(0, 0)
        self._offset = 0
        self._moveFromAngle = False
        self._moveFromRatio = False

    def moveWithoutStack(self, angle, ratio):
        self.setAngleAndRatio(angle, ratio)
        self.scene().parent().showTab()

    def mouseMoveEvent(self, event):
        if not self._isMoving:
            self._isMoving = True
            self._moveFromAngle = self._angle
            self._moveFromRatio = self._ratio
            self._linkToParentItem.setVisible(True)

        x = NODE_GRID(event.scenePos().x())
        y = NODE_GRID(event.scenePos().y())
        epos = Vector2(x, y) - self._offset
        eposToCenterVector = epos - self._center
        if eposToCenterVector.magnitude() == 0:
            self.setAngleAndRatio(0, 0)
        else:
            sinangle = (self._arcVector.rotate(pi / 2)).dot(eposToCenterVector)
            absangle = self._arcVector.angle(eposToCenterVector)
            angle = copysign(absangle, sinangle)
            ratio = eposToCenterVector.magnitude() / self._arcVector.magnitude()
            self.setAngleAndRatio(angle, ratio)

    def commitMove(self):
        self.scene().mainWindow.stack.push(
            MoveArcLabelItemCommand(self.scene(), self, self._moveFromAngle, self._moveFromRatio,
            self._angle, self._ratio))

    def setAngleAndRatio(self, angle, ratio):
        prevPos = self._center + self._ratio * self._arcVector.rotate(self._angle)
        newPos = self._center + ratio * self._arcVector.rotate(angle)
        dpos = newPos - prevPos
        self.moveBy(dpos.x, dpos.y)
        self._angle = angle
        self._ratio = ratio
        self.updatePos()

        rect = self.boundingRect()
        line = self._linkToParentItem.line()
        line.setP2(QPointF(self.pos().x() + rect.width() / 2, self.pos().y() + rect.height()))
        self._linkToParentItem.setLine(line)

    def getAngle(self):
        return self._angle

    def getRatio(self):
        return self._ratio

    def setArcVectorCenterAndOffset(self, arcVector, center, offset):
        self._arcVector = arcVector
        self._center = center
        self._offset = offset
        line = self._linkToParentItem.line()
        line.setP1(QPointF(center.x, center.y))
        self._linkToParentItem.setLine(line)
        self.updatePos()

    def updatePos(self):
        rect = self.boundingRect()
        pos = self._center + self._ratio * self._arcVector.rotate(self._angle) + self._offset
        self.setPos(pos.x - rect.width() / 2, pos.y - rect.height() / 2)