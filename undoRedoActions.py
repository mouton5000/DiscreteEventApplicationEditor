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


class MoveConnectedComponentCommand(QUndoCommand):
    def __init__(self, scene, component, prevPos, newPos, parent=None):
        super(MoveConnectedComponentCommand, self).__init__(parent)
        self._scene = scene
        self._component = component
        self._prevPos = prevPos
        self._newPos = newPos
        self._firstCall = True

    def undo(self):
        dvect = self._prevPos - self._newPos
        dx, dy = dvect.x, dvect.y
        self._component.setDXDY(dx, dy)
        self._scene.parent().showTab()

    def redo(self):
        if self._firstCall:
            self._firstCall = not self._firstCall
            return
        dvect = self._newPos - self._prevPos
        dx, dy = dvect.x, dvect.y
        self._component.setDXDY(dx, dy)
        self._scene.parent().showTab()


class ChangeConnectedComponentSceneCommand(QUndoCommand):
    def __init__(self, oldScene, component, newScene, parent=None):
        super(ChangeConnectedComponentSceneCommand, self).__init__(parent)
        self._oldScene = oldScene
        self._newScene = newScene
        self._component = component

    def undo(self):
        self.changeScene(self._newScene, self._oldScene)

    def redo(self):
        self.changeScene(self._oldScene, self._newScene)

    def changeScene(self, oldScene, newScene):
        self._component._scene = newScene
        for node in self._component.nodes:
            oldScene.nodes.remove(node)
            oldScene.removeItem(node._labelItem)
            newScene.addItem(node)
            newScene.addItem(node._labelItem)
            for a in node.outputArcs:
                oldScene.removeItem(a)
                oldScene.removeItem(a._labelItem)
                newScene.addItem(a)
                newScene.addItem(a._labelItem)
        oldScene.setSelected(None)
        self._component._scene.parent().showTab()
        self._component._scene.setSelected(self._component)


class ChangeInputOrOuputCommand(QUndoCommand):
    def __init__(self, scene, arc, inputNotOuput, oldNode, newNode, parent=None):
        super(ChangeInputOrOuputCommand, self).__init__(parent)
        self._scene = scene
        self._arc = arc
        self._inputNotOuput = inputNotOuput
        self._oldNode = oldNode
        self._newNode = newNode

    def undo(self):
        self._arc.changeNode(self._inputNotOuput, self._oldNode)

    def redo(self):
        self._arc.changeNode(self._inputNotOuput, self._newNode)