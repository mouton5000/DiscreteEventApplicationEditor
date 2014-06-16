from PyQt4.QtCore import Qt

__author__ = 'mouton'

from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QWidget, QLabel, QComboBox, QPushButton, QScrollArea


class PropertyWidget(QWidget):
    def __init__(self, parent=None):
        super(PropertyWidget, self).__init__(parent)
        self.layout = QVBoxLayout()

        self.noItem = QLabel('Proprietes de l\'element selectionne')
        self.noItem.setMinimumHeight(200)
        self.noItem.setMaximumHeight(200)

        self.arcParamEditor = ArcParamEditorWidget(self)
        self.nodeParamEditor = NodeParamEditorWidget(self)

        self.layout.addWidget(self.noItem)
        self.layout.addWidget(self.arcParamEditor)
        self.arcParamEditor.hide()
        self.layout.addWidget(self.nodeParamEditor)
        self.nodeParamEditor.hide()

        self.propertyItem = self.noItem

        self.setLayout(self.layout)

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


class ArcParamEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(ArcParamEditorWidget, self).__init__(parent)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox2 = QHBoxLayout()
        self._lb1 = QLabel('Indice de l\'arc : ', self)
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

        self.setMaximumHeight(200)

    def init(self):
        self._indexQCB.clear()
        self.setLabel('Etiquette de l\'arc.')
        self.setFormula('Formule d\'acceptance de l\'arc.')
        self.setConsequences('Consequences du passage par l\'arc.')

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

        vbox = QVBoxLayout()

        hboxTitle = QHBoxLayout()
        self._lb1 = QLabel('Indice du noeud : ', self)
        self._lb2 = QLabel('', self)
        self._lb2.setMinimumWidth(50)
        self._lb2.setMaximumWidth(50)
        hboxTitle.addWidget(self._lb1)
        hboxTitle.addWidget(self._lb2)

        self._labelTE = QLineEdit(self)
        hboxTitle.addWidget(self._labelTE)

        self._tokensTE = QTextEdit(self)
        self._tokensTE.setUndoRedoEnabled(True)
        vbox.addLayout(hboxTitle)
        vbox.addWidget(self._tokensTE)

        self.init()

        self._selectedNode = None
        self._labelTE.textChanged.connect(self.labelChanged)
        self._labelTE.textChanged.connect(self.window().setModified)

        self._tokensTE.textChanged.connect(self.tokenChanged)
        self._tokensTE.textChanged.connect(self.window().setModified)

        self.setMinimumHeight(200)
        self.setMaximumHeight(200)
        self.setLayout(vbox)

    def init(self):
        self.setLabel('Etiquette du noeud.')
        self.setTokens('Tokens du noeud')

    def setIndex(self, num):
        self._lb2.setText(str(num))

    def setLabel(self, label):
        self._labelTE.setText(label)

    def setTokens(self, tokens):
        self._tokensTE.setText(tokens)

    def labelChanged(self):
        try:
            self._selectedNode.setLabel(str(self._labelTE.text()))
        except AttributeError:
            pass

    def tokenChanged(self):
        try:
            self._selectedNode.setTokens(str(self._tokensTE.toPlainText()))
        except AttributeError:
            pass

    def setSelectedNode(self, n):
        self._selectedNode = n
        try:
            self.setIndex(n.num)
            self.setLabel(n.getLabel())
            self.setTokens(n.getTokensStr())
        except AttributeError:
            self.init()