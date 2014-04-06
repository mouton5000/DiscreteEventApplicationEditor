from PyQt4.QtGui import QUndoCommand


class AddItemCommand(QUndoCommand):
    def __init__(self, scene, item, firstCall=True, parent=None):
        super(AddItemCommand, self).__init__(parent)
        self._scene = scene
        self._item = item
        self._firstCall = firstCall

    def undo(self):
        self._scene.deleteItem(self._item)

    def redo(self):
        # The item cannot be inserted twice. We prevent the stack from calling redo automatically
        if self._firstCall:
            self._firstCall = not self._firstCall
            return

        self._scene.addItem(self._item)
        try:
            self._item.node1.outputArcs.append(self._item)
            self._item.node2.inputArcs.append(self._item)
        except AttributeError:
            pass


class DeleteItemCommand(QUndoCommand):
    def __init__(self, scene, item, parent=None):
        super(DeleteItemCommand, self).__init__(parent)
        self._opposite = AddItemCommand(scene, item, False, parent)

    def undo(self):
        self._opposite.redo()

    def redo(self):
        self._opposite.undo()


class MoveNodeCommand(QUndoCommand):
    def __init__(self, node, prevPos, newPos, parent=None):
        super(MoveNodeCommand, self).__init__(parent)
        self._node = node
        self._prevPos = prevPos
        self._newPos = newPos

    def undo(self):
        self._node.setXY(self._prevPos.x, self._prevPos.y)

    def redo(self):
        self._node.setXY(self._newPos.x, self._newPos.y)


class MoveArcCommand(QUndoCommand):
    def __init__(self, arc, prevCl, newCl, prevDelta=None, newDelta=None, parent=None):
        super(MoveArcCommand, self).__init__(parent)
        self._arc = arc
        self._prevCl = prevCl
        self._newCl = newCl
        if prevDelta and newDelta:
            self._prevDelta = prevDelta
            self._newDelta = newDelta

    def undo(self):
        try:
            self._arc.setClAndDelta(self._prevCl, self._prevDelta)
        except AttributeError:
            self._arc.setCl(self._prevCl)

    def redo(self):
        try:
            self._arc.setClAndDelta(self._newCl, self._newDelta)
        except AttributeError:
            self._arc.setCl(self._newCl)


class MoveArcLabelCommand(QUndoCommand):
    def __init__(self, arcLabel, prevOffset, newOffset, parent=None):
        super(MoveArcLabelCommand, self).__init__(parent)
        self._arcLabel = arcLabel
        self._prevOffset = prevOffset
        self._newOffset = newOffset

    def undo(self):
        self._arcLabel.setOffset(self._prevOffset)

    def redo(self):
        self._arcLabel.setOffset(self._newOffset)


class SetActiveNodeCommand(QUndoCommand):
    def __init__(self, node, isActive, parent=None):
        super(SetActiveNodeCommand, self).__init__(parent)
        self._node = node
        self._isActive = isActive

    def undo(self):
        self._node.setActive(not self._isActive)

    def redo(self):
        self._node.setActive(self._isActive)