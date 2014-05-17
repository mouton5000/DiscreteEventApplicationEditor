__author__ = 'mouton'

from PyQt4.QtGui import QVBoxLayout, QAction, \
    QFileDialog, QMainWindow, QWidget, QDesktopWidget, QUndoStack, QMessageBox
from visual import vector
import json
import os.path
import game.gameWindow as gameWindow
from stateMachine import StateMachine, Node, Transition
from itertools import chain
from grammar.booleanExpressions import Property, Event
from EditorItem import ViewWidget
from PropertiesItems import ArcParamEditorWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        self.stack = QUndoStack()
        self.stack.indexChanged.connect(self.setModified)

        self._nodeDict = None
        self._stateMachine = StateMachine()

        self._modified = False
        self._currentFile = None
        self._lastSaveOpenFileDirectory = '/home'

    def init_ui(self):
        widget = MainWidget(self)
        self.setCentralWidget(widget)
        self.initMenu()

        self.setGeometry(0, 0, 800, 640)
        self.setWindowTitle('GraphEditor')
        self.center()
        self.show()

    def initMenu(self):
        menubar = self.menuBar()

        newAction = QAction('&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.new)

        saveAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)

        saveAsAction = QAction('&Save as...', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.triggered.connect(self.saveAs)

        loadAction = QAction('&Load', self)
        loadAction.setShortcut('Ctrl+O')
        loadAction.triggered.connect(self.load)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(loadAction)

        undoAction = QAction('&Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.triggered.connect(self.undo)

        redoAction = QAction('&Redo', self)
        redoAction.setShortcut('Ctrl+Shift+Z')
        redoAction.triggered.connect(self.redo)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)

        compileAction = QAction('&Compile', self)
        compileAction.setShortcut('Shift+F9')
        compileAction.triggered.connect(self.compile)

        runAction = QAction('&Run', self)
        runAction.setShortcut('Shift+F10')
        runAction.triggered.connect(self.run)

        debugAction = QAction('&Debug', self)
        debugAction.setShortcut('Shift+F11')
        debugAction.triggered.connect(self.debug)

        stopAction = QAction('&Stop', self)
        stopAction.triggered.connect(self.stop)

        runMenu = menubar.addMenu('&Run')
        runMenu.addAction(compileAction)
        runMenu.addAction(runAction)
        runMenu.addAction(debugAction)
        runMenu.addAction(stopAction)

    def scene(self):
        return self.centralWidget().drawing.scene()

    def reinit(self):
        self.stack.clear()
        self._stateMachine = StateMachine()
        self._modified = False
        self._currentFile = None

    def new(self):
        scene = self.scene()
        scene.clear()
        self.reinit()
        return scene

    def save(self):
        if self._currentFile:
            self.saveAs(self._lastSaveOpenFileDirectory + '/' + self._currentFile)
        else:
            self.saveAs()

    def saveAs(self, fname=None):
        try:
            if not fname:
                fname = str(QFileDialog.getSaveFileName(self, 'Choose save destination',
                                                        self._lastSaveOpenFileDirectory, 'JSON files (*.json)'))

            if fname[-5:] != '.json':
                fname += '.json'

            with open(fname, 'w') as f:
                scene = self.scene()
                nodes = scene.nodes

                def nodeDict(node):
                    d = dict()
                    xy = node.getXY()
                    d['x'], d['y'] = xy.x, xy.y
                    d['isActive'] = node.isActive()
                    return d

                def arcDict(arc):
                    d = dict()
                    d['n1'] = nodes.index(arc.node1)
                    d['n2'] = nodes.index(arc.node2)
                    d['cl'] = arc.getCl()
                    try:
                        d['delta'] = arc.getDelta()
                    except AttributeError:
                        pass
                    d['label'] = arc.getLabel()
                    d['formula'] = arc.getFormula()
                    d['consequences'] = arc.getConsequences()
                    offset = arc.getLabelItem().getOffset()
                    d['labelItemOffset'] = [offset.x, offset.y]
                    return d

                d = {
                    "nodes": [nodeDict(node) for node in nodes],
                    "arcs": [arcDict(arc) for arc in chain.from_iterable(node.outputArcs for node in nodes)]}
                json.dump(d, f)

                self._lastSaveOpenFileDirectory = os.path.dirname(fname)
                self.setCurrentFile(os.path.basename(fname))
        except IOError:
            pass

    def load(self):
        try:
            fname = str(QFileDialog.getOpenFileName(self, 'Choose file to open',
                                                    self._lastSaveOpenFileDirectory, 'JSON files (*.json)'))

            with open(fname) as f:
                d = json.load(f)

                scene = self.new()

                def addNode(node):
                    x = node['x']
                    y = node['y']
                    n = scene.addNode(x, y)
                    n.setActive(node['isActive'])
                    return n

                nodes = [addNode(node) for node in d['nodes']]

                def addArc(arc):
                    n1 = nodes[arc['n1']]
                    n2 = nodes[arc['n2']]
                    a = scene.addArc(n1, n2)
                    if n1 == n2:
                        a.setClAndDelta(arc['cl'], arc['delta'])
                    else:
                        a.setCl(arc['cl'])
                    a.setLabel(arc['label'])
                    a.setFormula(arc['formula'])
                    a.setConsequences(arc['consequences'])
                    lioff = arc['labelItemOffset']
                    a.getLabelItem().setOffset(vector(lioff[0], lioff[1]))

                for arc in d['arcs']:
                    addArc(arc)

                self._lastSaveOpenFileDirectory = os.path.dirname(fname)
                self.reinit()
                self.setCurrentFile(os.path.basename(fname))
        except IOError:
            pass

    def setCurrentFile(self, currentFile):
        self._currentFile = currentFile
        self.setWindowTitle('GraphEditor : ' + currentFile)
        self._modified = False

    def setModified(self):
        if not self._modified:
            self._modified = True
            self.setWindowTitle(self.windowTitle() + ' *')

    def undo(self):
        self.stack.undo()

    def redo(self):
        self.stack.redo()

    def compile(self):
        scene = self.scene()

        def compileNode(node):
            n = Node(node.num)

            return n

        self._nodeDict = {node: Node(node.num) for node in scene.nodes}

        def compileArc(a):
            n1 = self._nodeDict[a.node1]
            n2 = self._nodeDict[a.node2]
            Transition(n1, n2, a.getFormula(), a.getConsequences())

        for arc in chain.from_iterable(node.outputArcs for node in scene.nodes):
            compileArc(arc)

    def run(self):
        if not self._stateMachine or not self._nodeDict:
            return

        self._stateMachine.clearActiveStates()
        for node, compNode in self._nodeDict.iteritems():
            if node.isActive():
                self._stateMachine.addActiveState(compNode)

        Property.properties.clear()
        Event.events.clear()
        gameWindow.init()

        self._stateMachine.init()
        for i in xrange(600):
            self._stateMachine.tick()
            if not gameWindow.tick():
                self.stop()
                return

    def debug(self):
        if not self._stateMachine:
            return
        gameWindow.init()

    def stop(self):
        gameWindow.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        if not self._modified:
            return

        reply = QMessageBox.question(self, 'Graph Editor',
                                     'The current graph has been modified. Do you want to save the changes?',
                                     QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                     QMessageBox.Save)

        if reply == QMessageBox.Save:
            self.save()
            event.accept()
        elif reply == QMessageBox.Discard:
            event.accept()
        else:
            event.ignore()


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        vbox = QVBoxLayout()
        self.drawing = ViewWidget(self)
        self.params = ArcParamEditorWidget(self)
        self.drawing.setArcParamEditor(self.params)
        vbox.addWidget(self.drawing)
        vbox.addWidget(self.params)
        self.setLayout(vbox)
