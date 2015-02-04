from PyQt4.QtGui import QUndoCommand


class AddNodeItemCommand(QUndoCommand):
    def __init__(self, scene, nodeItem, parent=None):
        super(AddNodeItemCommand, self).__init__(parent)
        self._scene = scene
        self._nodeItem = nodeItem

    def undo(self):
        self._scene.removeNodeWithoutStack(self._nodeItem)

    def redo(self):
        self._scene.addNodeWithoutStack(self._nodeItem)


class RemoveNodeItemCommand(QUndoCommand):
    def __init__(self, scene, nodeItem, parent=None):
        super(RemoveNodeItemCommand, self).__init__(parent)
        self._opposite = AddNodeItemCommand(scene, nodeItem, parent)

    def undo(self):
        self._opposite.redo()

    def redo(self):
        self._opposite.undo()


class AddArcItemCommand(QUndoCommand):
    def __init__(self, scene, arcItem, parent=None):
        super(AddArcItemCommand, self).__init__(parent)
        self._scene = scene
        self._arcItem = arcItem

    def undo(self):
        self._scene.removeArcWithoutStack(self._arcItem)

    def redo(self):
        self._scene.addArcWithoutStack(self._arcItem)


class RemoveArcItemCommand(QUndoCommand):
    def __init__(self, scene, arcItem, parent=None):
        super(RemoveArcItemCommand, self).__init__(parent)
        self._opposite = AddArcItemCommand(scene, arcItem, parent)

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
        self._node.moveWithoutStack(self._prevPos)

    def redo(self):
        self._node.moveWithoutStack(self._newPos)


class MoveArcCommand(QUndoCommand):
    def __init__(self, scene, arc, prevCl, newCl, prevCycleCl, newCycleCl, prevDelta=None, newDelta=None, parent=None):
        super(MoveArcCommand, self).__init__(parent)
        self._scene = scene
        self._arc = arc
        self._prevCl = prevCl
        self._newCl = newCl
        self._prevCycleCl = prevCycleCl
        self._newCycleCl = newCycleCl
        self._prevDelta = prevDelta
        self._newDelta = newDelta

    def undo(self):
        self._arc.moveWithoutStack(self._prevCl, self._prevCycleCl, self._prevDelta)

    def redo(self):
        self._arc.moveWithoutStack(self._newCl, self._newCycleCl, self._newDelta)


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


class MoveConnectedComponentCommand(QUndoCommand):
    def __init__(self, scene, component, prevCenter, newCenter, parent=None):
        super(MoveConnectedComponentCommand, self).__init__(parent)
        self._scene = scene
        self._component = component
        self._prevCenter = prevCenter
        self._newCenter = newCenter

    def undo(self):
        print self._prevCenter
        self._component.moveWithoutStack(self._prevCenter)

    def redo(self):
        print self._newCenter
        self._component.moveWithoutStack(self._newCenter)


class ChangeConnectedComponentSceneCommand(QUndoCommand):
    def __init__(self, oldScene, component, newScene, parent=None):
        super(ChangeConnectedComponentSceneCommand, self).__init__(parent)
        self._oldScene = oldScene
        self._newScene = newScene
        self._component = component

    def undo(self):
        self._newScene.changeConnectedComponentSceneWithoutStack(self._component, self._oldScene)

    def redo(self):
        self._oldScene.changeConnectedComponentSceneWithoutStack(self._component, self._newScene)


class ChangeInputOrOuputCommand(QUndoCommand):
    def __init__(self, scene, arc, inputNotOuput, oldNode, newNode, parent=None):
        super(ChangeInputOrOuputCommand, self).__init__(parent)
        self._scene = scene
        self._arc = arc
        self._inputNotOuput = inputNotOuput
        self._oldNode = oldNode
        self._newNode = newNode

    def undo(self):
        if self._inputNotOuput:
            self._arc.changeInputWithoutStack(self._oldNode)
        else:
            self._arc.changeOutputWithoutStack(self._oldNode)

    def redo(self):
        if self._inputNotOuput:
            self._arc.changeInputWithoutStack(self._newNode)
        else:
            self._arc.changeOutputWithoutStack(self._newNode)