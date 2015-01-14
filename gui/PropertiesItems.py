# -*- coding: latin-1 -*-

__author__ = 'mouton'

from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QWidget, QLabel, QComboBox, QPushButton


class PropertyWidget(QWidget):
    def __init__(self, parent=None):
        super(PropertyWidget, self).__init__(parent)
        self.layout = QVBoxLayout()

        self.noItem = QLabel('Property of the selected element.')

        self.arcParamEditor = ArcParamEditorWidget(self)
        self.nodeParamEditor = NodeParamEditorWidget(self)
        self.connectedComponentParamEditor = ConnectedComponentParamEditorWidget(self)

        self.layout.addWidget(self.noItem)
        self.layout.addWidget(self.arcParamEditor)
        self.arcParamEditor.hide()
        self.layout.addWidget(self.nodeParamEditor)
        self.nodeParamEditor.hide()
        self.layout.addWidget(self.connectedComponentParamEditor)
        self.connectedComponentParamEditor.hide()

        self.propertyItem = self.noItem

        self.setLayout(self.layout)

        self.setMinimumHeight(250)
        self.setMaximumHeight(250)

    def setItem(self, item):
        self.propertyItem.hide()
        self.propertyItem = item
        self.propertyItem.show()
        return item

    def setNoItem(self):
        return self.setItem(self.noItem)

    def setArcItem(self):
        return self.setItem(self.arcParamEditor)

    def setNodeItem(self):
        return self.setItem(self.nodeParamEditor)

    def setConnectedComponentItem(self):
        return self.setItem(self.connectedComponentParamEditor)


class ArcParamEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(ArcParamEditorWidget, self).__init__(parent)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox2 = QHBoxLayout()
        self._lb1 = QLabel('Arc index : ', self)
        self._indexQCB = QComboBox(self)
        self._indexQCB.setMaxVisibleItems(5)
        hbox2.addWidget(self._lb1)
        hbox2.addWidget(self._indexQCB)

        self._labelTE = QTextEdit(self)
        self._labelTE.setUndoRedoEnabled(True)
        vbox.addLayout(hbox2)
        vbox.addWidget(self._labelTE)

        self._formulaTE = QTextEdit(self)
        self._formulaTE.setUndoRedoEnabled(True)
        self._consequencesTE = QTextEdit(self)
        self._consequencesTE.setUndoRedoEnabled(True)
        hbox.addLayout(vbox)
        hbox.addWidget(self._formulaTE)
        hbox.addWidget(self._consequencesTE)
        self.setLayout(hbox)

        self._selectedArc = None

        self._labelTE.textChanged.connect(self.labelChanged)
        self._formulaTE.textChanged.connect(self.formulaChanged)
        self._consequencesTE.textChanged.connect(self.consequencesChanged)

        self._indexQCB.currentIndexChanged.connect(self.window().setModified)
        self._labelTE.textChanged.connect(self.window().setModified)
        self._formulaTE.textChanged.connect(self.window().setModified)
        self._consequencesTE.textChanged.connect(self.window().setModified)

    def init(self):
        self._indexQCB.clear()
        self.setLabel('Arc label.')
        self.setFormula('Arc boolean formula.')
        self.setConsequences('Arc consequeneces.')

    def setIndexes(self, maxIndex, index):
        self._indexQCB.clear()
        for i in xrange(maxIndex):
            self._indexQCB.addItem(str(i))
        self._indexQCB.setCurrentIndex(index)

    def setLabel(self, label):
        self._labelTE.setText(label)

    def setFormula(self, formula):
        self._formulaTE.setText(formula)

    def setConsequences(self, consequences):
        self._consequencesTE.setText(consequences)

    def labelChanged(self):
        try:
            self._selectedArc.setLabel(str(self._labelTE.toPlainText()))
        except AttributeError:
            pass

    def formulaChanged(self):
        try:
            self._selectedArc.setFormula(str(self._formulaTE.toPlainText()))
        except AttributeError:
            pass

    def consequencesChanged(self):
        try:
            self._selectedArc.setConsequences(str(self._consequencesTE.toPlainText()))
        except AttributeError:
            pass

    def setSelectedArc(self, a):
        try:
            self._indexQCB.currentIndexChanged.disconnect(self._selectedArc.setIndex)
        except (AttributeError, TypeError):
            pass

        self._selectedArc = a
        try:
            self.setIndexes(a.getMaxIndex(), a.getIndex())
            self.setLabel(a.getLabel())
            self.setFormula(a.getFormula())
            self.setConsequences(a.getConsequencesStr())
            self._indexQCB.currentIndexChanged.connect(a.setIndex)
        except AttributeError:
            self.init()


class NodeParamEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(NodeParamEditorWidget, self).__init__(parent)

        self._tokenWidgets = []
        self._showTokenWidgetIndex = 0

        vbox = QVBoxLayout()

        hboxTitle = QHBoxLayout()
        self._lb1 = QLabel('Node index : ', self)
        self._lb2 = QLabel('', self)
        self._lb2.setMinimumWidth(50)
        self._lb2.setMaximumWidth(50)
        hboxTitle.addWidget(self._lb1)
        hboxTitle.addWidget(self._lb2)

        self._labelTE = QLineEdit(self)
        hboxTitle.addWidget(self._labelTE)

        vbox.addLayout(hboxTitle)

        self._vboxToken = QVBoxLayout()

        self._upToken = QPushButton('Up')
        self._upToken.setMaximumHeight(20)
        # self._upToken.setMaximumWidth(150)
        self._upToken.setEnabled(False)

        self._plusToken = QPushButton('+')
        # self._plusToken.setMaximumWidth(150)

        self._downToken = QPushButton('Down')
        self._downToken.setMaximumHeight(20)
        # self._downToken.setMaximumWidth(150)
        self._downToken.setEnabled(False)

        self._vboxToken.addWidget(self._upToken)
        self._vboxToken.addWidget(self._plusToken)
        self._vboxToken.addWidget(self._downToken)

        vbox.addLayout(self._vboxToken)

        self._upToken.clicked.connect(self.upToken)
        self._downToken.clicked.connect(self.downToken)
        self._plusToken.clicked.connect(self.addToken)

        self.init()

        self._selectedNode = None
        self._labelTE.textChanged.connect(self.labelChanged)
        self._labelTE.textChanged.connect(self.window().setModified)

        self.setLayout(vbox)

    def addToken(self):
        self._selectedNode.addToken()
        token = TokenWidget(len(self._tokenWidgets), parent=self)
        self._tokenWidgets.append(token)
        self._vboxToken.insertWidget(self._vboxToken.count() - 2, token)

        if len(self._tokenWidgets) >= 3:
            self._tokenWidgets[-3].hide()
            self._upToken.setEnabled(True)
            self._showTokenWidgetIndex += 1

    def removeToken(self, tokenWidget):
        tokenWidget.hide()
        self._tokenWidgets.remove(tokenWidget)
        self._selectedNode.removeToken(tokenWidget.index)
        for tW in self._tokenWidgets[tokenWidget.index:]:
            tW.index -= 1
        self._vboxToken.removeWidget(tokenWidget)

        self.updateTokenWidgetIndex()

    def updateTokenWidgetIndex(self):
        if len(self._tokenWidgets) <= 2:
            self._upToken.setEnabled(False)
            self._downToken.setEnabled(False)
            for tokW in self._tokenWidgets:
                tokW.show()
            self._plusToken.show()
            self._showTokenWidgetIndex = 0
            return

        maxIndex = len(self._tokenWidgets) - 1
        if maxIndex == self._showTokenWidgetIndex:
            self._showTokenWidgetIndex -= 1

        self._tokenWidgets[self._showTokenWidgetIndex].show()
        self._tokenWidgets[self._showTokenWidgetIndex + 1].show()
        if maxIndex - self._showTokenWidgetIndex == 1:
            self._plusToken.show()
        else:
            self._tokenWidgets[self._showTokenWidgetIndex + 2].show()

    def upToken(self):
        self._downToken.setEnabled(True)

        maxIndex = len(self._tokenWidgets) - 1
        if self._showTokenWidgetIndex == maxIndex - 1:
            self._plusToken.hide()
        else:
            self._tokenWidgets[self._showTokenWidgetIndex + 2].hide()

        self._showTokenWidgetIndex -= 1
        self._tokenWidgets[self._showTokenWidgetIndex].show()
        if self._showTokenWidgetIndex == 0:
            self._upToken.setEnabled(False)

    def downToken(self):
        self._upToken.setEnabled(True)
        maxIndex = len(self._tokenWidgets) - 1
        if self._showTokenWidgetIndex == maxIndex - 2:
            self._plusToken.show()
        else:
            self._tokenWidgets[self._showTokenWidgetIndex + 3].show()

        self._tokenWidgets[self._showTokenWidgetIndex].hide()
        self._showTokenWidgetIndex += 1
        if self._showTokenWidgetIndex == maxIndex - 1:
            self._downToken.setEnabled(False)

    def init(self):
        self.setLabel('Node label.')

    def setIndex(self, num):
        self._lb2.setText(str(num))

    def setLabel(self, label):
        self._labelTE.setText(label)

    def setTokens(self, tokens):
        for tokenWidget in self._tokenWidgets:
            tokenWidget.hide()
        self._upToken.setEnabled(False)
        self._downToken.setEnabled(False)
        del self._tokenWidgets[:]

        for token in tokens:
            tokenWidget = TokenWidget(len(self._tokenWidgets), parent=self)
            tokenWidget.setText(token)
            self._tokenWidgets.append(tokenWidget)
            self._vboxToken.insertWidget(self._vboxToken.count() - 2, tokenWidget)
            tokenWidget.hide()

        self._plusToken.show()
        if len(self._tokenWidgets) >= 3:
            self._upToken.setEnabled(True)
            self._tokenWidgets[-2].show()
            self._tokenWidgets[-1].show()
            self._showTokenWidgetIndex = len(tokens) - 2
        else:
            for tokenWidget in self._tokenWidgets:
                tokenWidget.show()
            self._showTokenWidgetIndex = 0

    def labelChanged(self):
        try:
            self._selectedNode.setLabel(str(self._labelTE.text()))
        except AttributeError:
            pass

    def tokenChanged(self, token):
        index = token.index
        text = token.text
        self._selectedNode.setToken(index, text)

    def setSelectedNode(self, n):
        self._selectedNode = n
        try:
            self.setIndex(n.num)
            self.setLabel(n.getLabel())
            self.setTokens(n.getTokens())
        except AttributeError:
            self.init()


class TokenWidget(QWidget):
    def __init__(self, index, parent=None):
        super(TokenWidget, self).__init__(parent)

        self._index = index
        hboxToken = QHBoxLayout()
        hboxToken.addWidget(QLabel('Token'))
        self._indexLabel = QLabel(str(index))
        hboxToken.addWidget(self._indexLabel)
        hboxToken.addWidget(QLabel('('))
        self._qte = QLineEdit()
        self._qte.setMinimumHeight(30)
        self._qte.setMaximumHeight(30)
        hboxToken.addWidget(self._qte)
        hboxToken.addWidget(QLabel(')'))
        removeButton = QPushButton('-')
        hboxToken.addWidget(removeButton)

        self.setLayout(hboxToken)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        removeButton.clicked.connect(self.remove)
        removeButton.clicked.connect(self.window().setModified)

        self._qte.textChanged.connect(self.update)
        self._qte.textChanged.connect(self.window().setModified)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index
        self._indexLabel.setText(str(index))

    @property
    def text(self):
        return self._qte.text()

    def setText(self, text):
        return self._qte.setText(text)

    def remove(self):
        self.parent().removeToken(self)

    def update(self):
        self.parent().tokenChanged(self)


class ConnectedComponentParamEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(ConnectedComponentParamEditorWidget, self).__init__(parent)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Scene : '))

        self._sceneQCB = QComboBox(self)
        self._sceneQCB.setMaxVisibleItems(5)
        hbox.addWidget(self._sceneQCB)

        self._sceneQCB.clear()
        self.setLayout(hbox)

    def initSceneQCB(self):
        try:
            self._sceneQCB.currentIndexChanged.disconnect(self.changeScene)
        except TypeError:
            pass
        sceneOfCC = self._selectedConnectedComponent.scene()
        self._sceneQCB.clear()
        i = 0
        for scene in self.parent().parent().scenes():
            self._sceneQCB.addItem(scene.getName())
            if scene == sceneOfCC:
                self._sceneQCB.setCurrentIndex(i)
            i += 1

        self._sceneQCB.currentIndexChanged.connect(self.changeScene)

    def setSelectedConnectedComponent(self, cc):
        self._selectedConnectedComponent = cc
        self.initSceneQCB()

    def changeScene(self, sceneIndex):
        self._selectedConnectedComponent.setScene(sceneIndex)
        self._sceneQCB.clear()
        self._selectedConnectedComponent = None
