from PyQt4.QtCore import QPointF
from PyQt4.QtGui import QGraphicsSimpleTextItem
from euclid import Vector2
from undoRedoActions import MoveLabelItemCommand


class LabelItem(QGraphicsSimpleTextItem):
    def __init__(self, parent=None, scene=None):
        super(LabelItem, self).__init__('', parent, scene)
        self._offset = Vector2(0, 0)
        self._center = Vector2(0, 0)
        self._isMoving = False
        self._moveFromOffset = False

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

    def commitMove(self):
        self.scene().mainWindow.stack.push(
            MoveLabelItemCommand(self.scene(), self, self._moveFromOffset, self._offset))

    def moveWithoutStack(self, offset):
        self.setOffset(offset)
        self.scene().parent().showTab()

    def mouseMoveEvent(self, event):
        if not self._isMoving:
            self._isMoving = True
            self._moveFromOffset = self._offset
            self._linkToParentItem.setVisible(True)

        epos = Vector2(event.scenePos().x(), event.scenePos().y())
        rect = self.boundingRect()
        pos = Vector2(self.pos().x() + rect.width() / 2, self.pos().y() + rect.height() / 2)
        center = pos - self._offset
        self.setOffset(epos - center)

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
        pos = self._center + self._offset
        self.setPos(pos.x, pos.y)