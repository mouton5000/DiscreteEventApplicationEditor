__author__ = 'mouton'

from PyQt4.QtGui import QVBoxLayout, QAction, \
    QFileDialog, QMainWindow, QWidget, QDesktopWidget, QUndoStack, QMessageBox, QHBoxLayout
from euclid import Vector2
import json
import os.path
import game.gameWindow as gameWindow
import stateMachine
from stateMachine import Transition
from itertools import chain
from PropertiesItems import PropertyWidget
from ScenesManagerItems import ViewsManagerWidget
from collections import deque
from gui.EditorItem import NodesIdsGenerator, ModeController
from gui.TabItem import TabbedEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        self.stack = QUndoStack()

        self.stack.indexChanged.connect(self.setModified)

        self._nodeDict = None

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

        newSceneAction = QAction('New Scene', self)
        newSceneAction.setShortcut('Ctrl+M')
        newSceneAction.triggered.connect(self.addNewScene)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(loadAction)
        fileMenu.addSeparator()
        fileMenu.addAction(newSceneAction)

        undoAction = QAction('&Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.triggered.connect(self.undo)

        redoAction = QAction('&Redo', self)
        redoAction.setShortcut('Ctrl+Shift+Z')
        redoAction.triggered.connect(self.redo)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)

        runAction = QAction('&Run', self)
        runAction.setShortcut('Shift+F10')
        runAction.triggered.connect(self.run)

        debugAction = QAction('&Debug', self)
        debugAction.setShortcut('Shift+F11')
        debugAction.triggered.connect(self.debug)

        stopAction = QAction('&Stop', self)
        stopAction.triggered.connect(self.stop)

        runMenu = menubar.addMenu('&Run')
        runMenu.addAction(runAction)
        runMenu.addAction(debugAction)
        runMenu.addAction(stopAction)

    def scenes(self):
        return self.centralWidget().scenes()

    def addNewScene(self):
        self.centralWidget().addScene()

    def addScenes(self, scenesDesc):
        return (self.centralWidget().addNamedScene(sceneDesc['name']) for sceneDesc in scenesDesc)

    def settingsWidget(self):
        return self.centralWidget().settingsWidget()

    def getNodesIdGenerator(self):
        return self.centralWidget().getNodesIdsGenerator()

    def reinit(self):
        self.stack.clear()
        stateMachine.clear()
        self.setCurrentFile(None)
        self._modified = False
        self.centralWidget().reinit()

    def new(self):
        self._new(True)

    def newFromLoad(self):
        self._new(False)

    def _new(self, doCheckSave):
        if doCheckSave and not self.checkSave():
            return
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
            d['cycleCl'] = arc.getCycleCl()
            d['delta'] = arc.getDelta()
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
        settingsDict = {"fps": int(setW.getFPS()), "maxTick": int(setW.getMaxTick()), "width": int(setW.getWidth()),
                        "height": int(setW.getHeight()), "spritesRegistery": setW.getSprites(),
                        "soundsRegistery": setW.getSounds()}

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
        if not self.checkSave():
            return
        try:
            fname = str(QFileDialog.getOpenFileName(self, 'Choose file to open',
                                                    self._lastSaveOpenFileDirectory, 'JSON files (*.json)'))

            with open(fname) as f:
                d = json.load(f)

                self._lastSaveOpenFileDirectory = os.path.dirname(fname)
                self.newFromLoad()
                self.setCurrentFile(os.path.basename(fname))
        except IOError:
            return

        def addNode(node, scene):
            x = node['x']
            y = node['y']
            n = scene.addNode(x, y)
            n.num = node['num']
            n.setLabel(node['label'])
            n.setTokens(node['tokens'])
            lioff = node['labelItemOffset']
            n.getLabelItem().setOffset(Vector2(lioff[0], lioff[1]))
            return n

        def addArc(arc, scene, nodes):
            n1 = nodes[arc['n1']]
            n2 = nodes[arc['n2']]
            a = scene.addArc(n1, n2)
            a.setCl(arc['cl'])
            a.setCycleCl(arc['cycleCl'])
            a.setDelta(arc['delta'])
            a.setLabel(arc['label'])
            a.setFormula(arc['formula'])
            a.setConsequences(arc['consequences'])
            lioff = arc['labelItemOffset']
            a.getLabelItem().setOffset(Vector2(lioff[0], lioff[1]))
            a.drawPath()

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
            setW.setMaxTick(settingsDict['maxTick'])
            setW.setWidth(settingsDict['width'])
            setW.setHeight(settingsDict['height'])
            setW.setSprites(settingsDict['spritesRegistery'])
            setW.setSounds(settingsDict['soundsRegistery'])

            self.stack.clear()

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

    def run(self):

        stateMachine.clearNodes()
        stateMachine.clearTokens()

        DEBUG = False

        def compileNode(node):
            return stateMachine.addNode(node.num, str(node.num) + ':' + str(node.getLabel()))

        def compileArc(a):
            n1 = self._nodeDict[a.node1]
            n2 = self._nodeDict[a.node2]
            Transition(n1, n2, a.getFormula(), a.getConsequences())

        self._nodeDict = {}
        for scene in self.scenes():
            self._nodeDict.update({node: compileNode(node) for node in scene.nodes})
            for arc in chain.from_iterable(node.outputArcs for node in scene.nodes):
                compileArc(arc)

        stateMachine.init()
        for node, compNode in self._nodeDict.iteritems():
            for token in node.getTokens():
                stateMachine.addToken(compNode, token)

        setW = self.settingsWidget()
        fps = setW.getFPS()
        maxTick = setW.getMaxTick()
        width = setW.getWidth()
        height = setW.getHeight()
        spritesDictionnary = setW.getSpritesDictionnary()
        soundsDictionnary = setW.getSoundsDictionnary()
        rootDir = self._lastSaveOpenFileDirectory

        gameWindow.init(fps, width, height, spritesDictionnary, soundsDictionnary, rootDir)

        frame = 0
        tick = 0
        while maxTick <= 0 or tick < maxTick:
            retick = True
            while retick and (maxTick <= 0 or tick < maxTick):
                if DEBUG:
                    print frame, tick
                tick += 1
                retick = stateMachine.tick(debug=DEBUG)
            frame += 1
            stateMachine.updateTokensNbFrames()
            if not gameWindow.tick():
                break
        self.stop()

    def debug(self):
        pass

    def stop(self):
        try:
            gameWindow.hide()
        except AttributeError:
            pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        if self.checkSave():
            event.accept()
        else:
            event.ignore()

    def checkSave(self):
        if not self._modified:
            return True

        reply = QMessageBox.question(self, 'Graph Editor',
                                     'The current graph has been modified. Do you want to save the changes?',
                                     QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                     QMessageBox.Save)

        if reply == QMessageBox.Save:
            self.save()
            return True
        else:
            return reply == QMessageBox.Discard


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        self._nodesIdsGenerator = NodesIdsGenerator()
        self._modeController = ModeController(mainWindow=self.parent())

        self._propertiesEditor = PropertyWidget(self)
        self._viewsManager = \
            ViewsManagerWidget(parent=self, propertiesEditor=self._propertiesEditor, mainWindow=self.parent(),
                               nodesIdsGenerator=self._nodesIdsGenerator, modeController=self._modeController)
        self._tabItem = TabbedEditor(self._propertiesEditor, parent=self, mainWindow=self.parent(),
                                     nodesIdsGenerator=self._nodesIdsGenerator, modeController=self._modeController)

        vbox.addWidget(self._tabItem)
        vbox.addWidget(self._propertiesEditor)

        hbox.addWidget(self._viewsManager)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        self._machin = 0

    def viewsManager(self):
        return self._viewsManager

    def tabItem(self):
        return self._tabItem

    def scenes(self):
        return self._viewsManager.scenes()

    def addScene(self):
        return self._viewsManager.addView().scene()

    def addNamedScene(self, name):
        return self._viewsManager.addNamedView(name).scene()

    def settingsWidget(self):
        return self._tabItem.settingsWidget()

    def reinit(self):
        self._nodesIdsGenerator.reinit()
        self._tabItem.reinit()
        self._viewsManager.reinit()

    def getNodesIdsGenerator(self):
        return self._nodesIdsGenerator
