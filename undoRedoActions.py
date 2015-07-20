from PyQt4.QtGui import QUndoCommand


class AddNodeItemCommand(QUndoCommand):
    def __init__(self, scene, nodeItem, parent=None):
        super(AddNodeItemCommand, self).__init__(parent)
        self._scene = scene
        self._nodeItem = nodeItem

    def undo(self):
        self._scene.removeNodeWithoutStack(self._nodeItem, [])

    def redo(self):
        self._scene.addNodeWithoutStack(self._nodeItem)


class RemoveNodeItemCommand(QUndoCommand):
    def __init__(self, scene, nodeItem, parent=None):
        super(RemoveNodeItemCommand, self).__init__(parent)
        self._scene = scene
        self._nodeItem = nodeItem
        from copy import copy
        self._arcsItems = set(copy(nodeItem.outputArcs) + copy(nodeItem.inputArcs))

    def undo(self):
        self._scene.undoRemoveNodeWithoutStack(self._nodeItem, self._arcsItems)

    def redo(self):
        self._scene.removeNodeWithoutStack(self._nodeItem, self._arcsItems)


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


class MergeNodesCommand(QUndoCommand):
    def __init__(self, scene, fromNode, toNode, parent=None):
        super(MergeNodesCommand, self).__init__(parent)
        self._scene = scene
        self._fromNode = fromNode
        self._toNode = toNode
        from copy import copy
        self._inputArcsOfFromNodes = copy(fromNode.inputArcs)
        self._outputArcsOfFromNodes = copy(fromNode.outputArcs)

    def undo(self):
        self._scene.unmergeNodesWithoutStack(self._fromNode, self._inputArcsOfFromNodes, self._outputArcsOfFromNodes)

    def redo(self):
        self._scene.mergeNodesWithoutStack(self._fromNode, self._toNode,
                                           self._inputArcsOfFromNodes, self._outputArcsOfFromNodes)


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


class MoveNodeLabelItemCommand(QUndoCommand):
    def __init__(self, scene, labelItem, prevOffset, newOffset, parent=None):
        super(MoveNodeLabelItemCommand, self).__init__(parent)
        self._scene = scene
        self._labelItem = labelItem
        self._prevOffset = prevOffset
        self._newOffset = newOffset

    def undo(self):
        self._labelItem.moveWithoutStack(self._prevOffset)

    def redo(self):
        self._labelItem.moveWithoutStack(self._newOffset)


class MoveArcLabelItemCommand(QUndoCommand):
    def __init__(self, scene, labelItem, prevAngle, prevRatio, newAngle, newRatio, parent=None):
        super(MoveArcLabelItemCommand, self).__init__(parent)
        self._scene = scene
        self._labelItem = labelItem
        self._prevAngle = prevAngle
        self._prevRatio = prevRatio
        self._newAngle = newAngle
        self._newRatio = newRatio

    def undo(self):
        self._labelItem.moveWithoutStack(self._prevAngle, self._prevRatio)

    def redo(self):
        self._labelItem.moveWithoutStack(self._newAngle, self._newRatio)


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


class RemoveConnectedComponentCommand(QUndoCommand):
    def __init__(self, scene, component, parent=None):
        super(RemoveConnectedComponentCommand, self).__init__(parent)
        self._scene = scene
        self._component = component

    def undo(self):
        self._scene.addConnectedComponentWithoutStack(self._component)

    def redo(self):
        self._scene.removeConnectedComponentWithoutStack(self._component)


class CopyConnectedComponentCommand(QUndoCommand):
    def __init__(self, scene, component, x, y, parent=None):
        super(CopyConnectedComponentCommand, self).__init__(parent)
        self._scene = scene
        self._component = component
        self._x = x
        self._y = y
        self._copyComponent = None

    def undo(self):
        if self._copyComponent is not None:
            self._scene.removeConnectedComponentWithoutStack(self._copyComponent)

    def redo(self):
        self._copyComponent = self._scene.copyConnectedComponentWithoutStack(self._component, self._x, self._y)