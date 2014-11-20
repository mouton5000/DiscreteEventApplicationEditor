from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QWidget, QLabel, QComboBox, QPushButton
__author__ = 'mouton'


class SettingsWidget(QWidget):
    def __init__(self, parent=None, mainWindow=None):
        super(SettingsWidget, self).__init__(parent)
        self.mainWindow = mainWindow

        # self._fps = 60
        # self._registery = []
        # self._width = 800
        # self._height = 640

        vbox = QVBoxLayout()

        self._spriteWidgets = []
        self._showSpritesWidgetIndex = 0

        self._fpsTE = QLineEdit(self)

        hboxSize = QHBoxLayout()
        self._widthTE = QLineEdit(self)
        self._heightTE = QLineEdit(self)

        hboxSize.addWidget(self._widthTE)
        hboxSize.addWidget(self._heightTE)

        vbox.addWidget(self._fpsTE)
        vbox.addLayout(hboxSize)

        self._vboxSprites = QVBoxLayout()

        self._upSprites = QPushButton('Up')
        self._upSprites.setMaximumHeight(20)
        self._upSprites.setEnabled(False)

        self._plusSprites = QPushButton('+')

        self._downSprites = QPushButton('Down')
        self._downSprites.setMaximumHeight(20)
        self._downSprites.setEnabled(False)

        self._vboxSprites.addWidget(self._upSprites)
        self._vboxSprites.addWidget(self._plusSprites)
        self._vboxSprites.addWidget(self._downSprites)

        vbox.addLayout(self._vboxSprites)

        self._upSprites.clicked.connect(self.upSprites)
        self._downSprites.clicked.connect(self.downSprites)
        self._plusSprites.clicked.connect(self.addSprite)

        self.init()

        self._fpsTE.textChanged.connect(self.fpsChanged)
        self._fpsTE.textChanged.connect(self.window().setModified)
        self._widthTE.textChanged.connect(self.widthChanged)
        self._widthTE.textChanged.connect(self.window().setModified)
        self._heightTE.textChanged.connect(self.heightChanged)
        self._heightTE.textChanged.connect(self.window().setModified)

        self.setLayout(vbox)

    def addSprite(self):
        sprite = SpriteWidget(len(self._spriteWidgets), parent=self)
        self._spriteWidgets.append(sprite)
        self._vboxSprites.insertWidget(self._vboxSprites.count() - 2, sprite)

        if len(self._spriteWidgets) >= 3:
            self._spriteWidgets[-3].hide()
            self._upSprites.setEnabled(True)
            self._showSpritesWidgetIndex += 1

    def removeSprite(self, spriteWidget):
        spriteWidget.hide()
        self._spriteWidgets.remove(spriteWidget)
        #self._selectedNode.removeSprites(spriteWidget.index)
        for tW in self._spriteWidgets[spriteWidget.index:]:
            tW.index -= 1
        self._vboxSprites.removeWidget(spriteWidget)

        self.updateSpritesWidgetIndex()

    def updateSpritesWidgetIndex(self):
        if len(self._spriteWidgets) <= 2:
            self._upSprites.setEnabled(False)
            self._downSprites.setEnabled(False)
            for sprW in self._spriteWidgets:
                sprW.show()
            self._plusSprites.show()
            self._showSpritesWidgetIndex = 0
            return

        maxIndex = len(self._spriteWidgets) - 1
        if maxIndex == self._showSpritesWidgetIndex:
            self._showSpritesWidgetIndex -= 1

        self._spriteWidgets[self._showSpritesWidgetIndex].show()
        self._spriteWidgets[self._showSpritesWidgetIndex + 1].show()
        if maxIndex - self._showSpritesWidgetIndex == 1:
            self._plusSprites.show()
        else:
            self._spriteWidgets[self._showSpritesWidgetIndex + 2].show()

    def upSprites(self):
        self._downSprites.setEnabled(True)

        maxIndex = len(self._spriteWidgets) - 1
        if self._showSpritesWidgetIndex == maxIndex - 1:
            self._plusSprites.hide()
        else:
            self._spriteWidgets[self._showSpritesWidgetIndex + 2].hide()

        self._showSpritesWidgetIndex -= 1
        self._spriteWidgets[self._showSpritesWidgetIndex].show()
        if self._showSpritesWidgetIndex == 0:
            self._upSprites.setEnabled(False)

    def downSprites(self):
        self._upSprites.setEnabled(True)
        maxIndex = len(self._spriteWidgets) - 1
        if self._showSpritesWidgetIndex == maxIndex - 2:
            self._plusSprites.show()
        else:
            self._spriteWidgets[self._showSpritesWidgetIndex + 3].show()

        self._spriteWidgets[self._showSpritesWidgetIndex].hide()
        self._showSpritesWidgetIndex += 1
        if self._showSpritesWidgetIndex == maxIndex - 1:
            self._downSprites.setEnabled(False)

    def init(self):
        self._fpsTE.setText('60')
        self._heightTE.setText('640')
        self._widthTE.setText('800')

    def fpsChanged(self):
        pass

    def widthChanged(self):
        pass

    def heightChanged(self):
        pass


class SpriteWidget(QWidget):
    def __init__(self, index, parent=None):
        super(SpriteWidget, self).__init__(parent)

        self._index = index
        hboxToken = QHBoxLayout()
        self._spriteIDTE = QLineEdit('Sprite ' + str(self._index) + ' ID')
        self._spriteIDTE.setMinimumHeight(30)
        self._spriteIDTE.setMaximumHeight(30)
        self._spriteFilePathTE = QLineEdit('Sprite ' + str(self._index) + ' File Path')
        self._spriteFilePathTE.setMinimumHeight(30)
        self._spriteFilePathTE.setMaximumHeight(30)
        hboxToken.addWidget(self._spriteIDTE)
        hboxToken.addWidget(self._spriteFilePathTE)
        removeButton = QPushButton('-')
        hboxToken.addWidget(removeButton)

        self.setLayout(hboxToken)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        removeButton.clicked.connect(self.remove)
        removeButton.clicked.connect(self.window().setModified)

        #self._qte.textChanged.connect(self.update)
        #self._qte.textChanged.connect(self.window().setModified)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index
        #self._indexLabel.setText(str(index))

    @property
    def text(self):
        #return self._qte.text()
        pass

    def setText(self, text):
        #return self._qte.setText(text)
        pass

    def remove(self):
        self.parent().removeSprite(self)

    def update(self):
        #self.parent().spriteChanged(self)
        pass


