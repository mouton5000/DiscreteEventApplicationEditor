from PyQt4.QtGui import QUndoCommand


class AddItemCommand(QUndoCommand):
    def __init__(self, scene, item, firstCall=True, parent=None):
        super(AddItemCommand, self).__init__(parent)
        self._scene = scene
        self._item = item
        self._firstCall = firstCall

    def undo(self):
        self._scene.deleteItem(self._item)
        self._scene.parent().showTab()

    def redo(self):
        # The item cannot be inserted twice. We prevent the stack from calling redo automatically
        if self._firstCall:
            self._firstCall = not self._firstCall
            return

        self._scene.addItem(self._item)
        self._scene.parent().showTab()

        try:
            self._item.num = self._scene.getNextNodeId()
        except AttributeError:
            pass

        try:
            self._item.node1.outputArcs.append(self._item)
            self._item.node2.inputArcs.append(self._item)
        except AttributeError:
            pass

        try:
            self._scene.addItem(self._item._labelItem)
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
    def __init__(self, scene, node, prevPos, newPos, parent=None):
        super(MoveNodeCommand, self).__init__(parent)
        self._scene = scene
        self._node = node
        self._prevPos = prevPos
        self._newPos = newPos

    def undo(self):
        self._node.setXY(self._prevPos.x, self._prevPos.y)
        self._scene.parent().showTab()

    def redo(self):
        self._node.setXY(self._newPos.x, self._newPos.y)
        self._scene.parent().showTab()


class MoveArcCommand(QUndoCommand):
    def __init__(self, scene, arc, prevCl, newCl, prevDelta=None, newDelta=None, parent=None):
        super(MoveArcCommand, self).__init__(parent)
        self._scene = scene
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
        self._scene.parent().showTab()

    def redo(self):
        try:
            self._arc.setClAndDelta(self._newCl, self._newDelta)
        except AttributeError:
            self._arc.setCl(self._newCl)
        self._scene.parent().showTab()


class MoveLabelItemCommand(QUndoCommand):
    def __init__(self, scene, labelItem, prevOffset, newOffset, parent=None):
        super(MoveLabelItemCommand, self).__init__(parent)
        self._scene = scene
        self._labelItem = labelItem
        self._prevOffset = prevOffset
        self._newOffset = newOffset

    def undo(self):
        self._labelItem.setOffset(self._prevOffset)
        self._scene.parent().showTab()

    def redo(self):
        self._labelItem.setOffset(self._newOffset)
        self._scene.parent().showTab()