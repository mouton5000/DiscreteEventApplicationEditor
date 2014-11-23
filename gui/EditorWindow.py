from collections import deque
from gui.EditorItem import NodesIdsGenerator, ModeController
from gui.TabItem import TabbedEditor

__author__ = 'mouton'

from PyQt4.QtGui import QVBoxLayout, QAction, \
    QFileDialog, QMainWindow, QWidget, QDesktopWidget, QUndoStack, QMessageBox
from visual import vector
import json
import os.path
import game.gameWindow as gameWindow
from stateMachine import StateMachine, Transition
from itertools import chain
from PropertiesItems import PropertyWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        self.stack = QUndoStack()

        self.stack.indexChanged.connect(self.setModified)

        self._nodeDict = None
        self._stateMachine = StateMachine()

        self.setCurrentFile(None)
        self._lastSaveOpenFileDirectory = '/home'

    def init_ui(self):
        self._loading = False
        self._modified = False

        widget = MainWidget(self)
        self.setCentralWidget(widget)
        self.initMenu()

        self.setGeometry(0, 0, 800, 640)
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

    def scenes(self):
        return self.centralWidget().scenes()

    def addScenes(self, scenesDesc):
        return (self.centralWidget().addScene(sceneDesc['name']) for sceneDesc in scenesDesc)

    def settingsWidget(self):
        return self.centralWidget().settingsWidget()

    def getNodesIdGenerator(self):
        return self.centralWidget().getNodesIdsGenerator()

    def reinit(self):
        self.stack.clear()
        self._stateMachine = StateMachine()
        self.setCurrentFile(None)
        self._modified = False
        self.centralWidget().reinit()

    def new(self):
        scenes = self.scenes()
        for scene in scenes:
            scene.clear()
        self.reinit()

    def save(self):
        if self._currentFile:
            self.saveAs(self._lastSaveOpenFileDirectory + '/' + self._currentFile)
        else:
            self.saveAs()

    def saveAs(self, fname=None):
        if not fname:
            fname = str(QFileDialog.getSaveFileName(self, 'Choose save destination',
                                                    self._lastSaveOpenFileDirectory, 'JSON files (*.json)'))

        if fname[-5:] != '.json':
            fname += '.json'

        def nodeDict(node):
            d = dict()
            xy = node.getXY()
            d['x'], d['y'] = xy.x, xy.y
            # d['isActive'] = node.isActive()
            d['num'] = node.num
            d['label'] = node.getLabel()
            d['tokens'] = node.getTokens()
            offset = node.getLabelItem().getOffset()
            d['labelItemOffset'] = [offset.x, offset.y]
            return d

        def arcDict(nodes, arc):
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

        def sceneDict(scene):
            nodes = scene.nodes
            return {"name": str(scene.getName()),
                    "nodes": [nodeDict(node) for node in nodes],
                    "arcs": [arcDict(nodes, arc) for arc in chain.from_iterable(node.outputArcs
                                                                                for node in nodes)]}

        nig = self.getNodesIdGenerator()
        l = [sceneDict(scene) for scene in self.scenes()]

        setW = self.settingsWidget()
        settingsDict = {"fps": int(setW.getFPS()), "width": int(setW.getWidth()),
                        "height": int(setW.getHeight()), "spritesRegistery": setW.getSprites()}

        d = {"nodeId": nig.getNodeId(),
             "nextIds": list(nig.getNextIds()),
             "scenes": l,
             "settings": settingsDict}

        try:
            with open(fname, 'w') as f:
                json.dump(d, f)

                self._lastSaveOpenFileDirectory = os.path.dirname(fname)
                self.setCurrentFile(os.path.basename(fname))
        except IOError:
            return

    def load(self):
        try:
            fname = str(QFileDialog.getOpenFileName(self, 'Choose file to open',
                                                    self._lastSaveOpenFileDirectory, 'JSON files (*.json)'))

            with open(fname) as f:
                d = json.load(f)

                self._lastSaveOpenFileDirectory = os.path.dirname(fname)
                self.new()
                self.setCurrentFile(os.path.basename(fname))
        except IOError:
            return

        def addNode(node, scene):
            x = node['x']
            y = node['y']
            # n.setActive(node['isActive'])
            n = scene.addNode(x, y)
            n.num = node['num']
            n.setLabel(node['label'])
            n.setTokens(node['tokens'])
            lioff = node['labelItemOffset']
            n.getLabelItem().setOffset(vector(lioff[0], lioff[1]))
            return n

        def addArc(arc, scene, nodes):
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

        class LoadingWith():
            def __init__(self, mainWindow):
                self._mainWindow = mainWindow

            def __enter__(self):
                self._mainWindow._loading = True

            def __exit__(self, *_):
                self._mainWindow._loading = False

        with LoadingWith(self):
            scenesDesc = d['scenes']
            scenes = self.addScenes(scenesDesc)

            for scene, sceneDesc in zip(scenes, scenesDesc):
                nodes = [addNode(node, scene) for node in sceneDesc['nodes']]

                for arc in sceneDesc['arcs']:
                    addArc(arc, scene, nodes)

                scene.setSelected(None)

            nig = self.getNodesIdGenerator()
            nig.setNodeId(d['nodeId'])
            nig.setNextIds(deque(d['nextIds']))

            settingsDict = d['settings']
            setW = self.settingsWidget()
            setW.setFPS(settingsDict['fps'])
            setW.setWidth(settingsDict['width'])
            setW.setHeight(settingsDict['height'])
            for num, filePath in settingsDict['spritesRegistery']:
                setW.addSpriteWithValues(num, filePath)

    def setCurrentFile(self, currentFile):
        self._currentFile = currentFile
        if currentFile is None:
            self.setWindowTitle('GraphEditor')
        else:
            self.setWindowTitle('GraphEditor : ' + currentFile)
        self._modified = False

    def setModified(self):
        if self._loading:
            return
        if not self._modified:
            self._modified = True
            self.setWindowTitle(self.windowTitle() + ' *')

    def undo(self):
        self.stack.undo()

    def redo(self):
        self.stack.redo()

    def compile(self):
        self._stateMachine.clearNodes()
        self._stateMachine.clearTokens()

        def compileNode(node):
            return self._stateMachine.addNode(node.num, str(node.num) + ':' + str(node.getLabel()))

        def compileArc(a):
            n1 = self._nodeDict[a.node1]
            n2 = self._nodeDict[a.node2]
            Transition(n1, n2, a.getFormula(), a.getConsequences())

        for scene in self.scenes():
            self._nodeDict = {node: compileNode(node) for node in scene.nodes}
            for arc in chain.from_iterable(node.outputArcs for node in scene.nodes):
                compileArc(arc)

    def run(self):
        if not self._stateMachine or not self._nodeDict:
            return

        setW = self.settingsWidget()
        fps = setW.getFPS()
        width = setW.getWidth()
        height = setW.getHeight()
        spritesRegistery = setW.getSpritesRegistery()

        self._gw = gameWindow.GameWindow(fps, width, height, spritesRegistery)

        self._stateMachine.init(self._gw)
        for node, compNode in self._nodeDict.iteritems():
            for token in node.getTokens():
                self._stateMachine.addToken(compNode, token)

        i = 0
        while True:
        #for i in xrange(600):
            print i
            i += 1
            retick = True
            while retick:
                retick = self._stateMachine.tick()
            self._stateMachine.updateTokensNbFrames()
            if not self._gw.tick():
                break
        self.stop()

    def debug(self):
        pass
        # if not self._stateMachine:
        #     return
        # gameWindow.init()

    def stop(self):
        try:
            self._gw.hide()
        except AttributeError:
            pass

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
        self.nodesIdsGenerator = NodesIdsGenerator()
        self.modeController = ModeController(mainWindow=self.parent())
        self.propertiesEditor = PropertyWidget(self)

        self.drawing = TabbedEditor(self.propertiesEditor, parent=self, mainWindow=self.parent(),
                                    nodesIdsGenerator=self.nodesIdsGenerator, modeController=self.modeController)
        vbox.addWidget(self.drawing)
        vbox.addWidget(self.propertiesEditor)
        self.setLayout(vbox)

    def scenes(self):
        return self.drawing.scenes()

    def addScene(self, name):
        return self.drawing.insertTabbedView(name=name).scene()

    def settingsWidget(self):
        return self.drawing.settingsWidget()

    def reinit(self):
        self.nodesIdsGenerator.reinit()
        self.drawing.reinit()

    def getNodesIdsGenerator(self):
        return self.nodesIdsGenerator

    # def __init__(self, parent=None):
    #     super(MainWidget, self).__init__(parent)
    #
    #     vbox = QVBoxLayout()
    #     self.drawing = ViewWidget(parent=self, mainWindow=self.parent())
    #     self.propertiesEditor = PropertyWidget(self)
    #     self.drawing.setPropertiesEditor(self.propertiesEditor)
    #     vbox.addWidget(self.drawing)
    #     vbox.addWidget(self.propertiesEditor)
    #     self.setLayout(vbox)
    #
    # def scene(self):
    #     return self.drawing.scene()
