from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton

__author__ = 'mouton'


class SettingsWidget(QWidget):

    DEFAULT_FPS = 60
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 640

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
        self._plusSprites.clicked.connect(self.window().setModified)

        self.init()

        self._fpsTE.textChanged.connect(self.window().setModified)
        self._widthTE.textChanged.connect(self.window().setModified)
        self._heightTE.textChanged.connect(self.window().setModified)

        self.setLayout(vbox)

    def getSprites(self):
        return [(str(sprW.getNum()), str(sprW.getFilePath())) for sprW in self._spriteWidgets]

    def addSprite(self):
        sprite = SpriteWidget(parent=self)
        self._spriteWidgets.append(sprite)
        self._vboxSprites.insertWidget(self._vboxSprites.count() - 2, sprite)

        if len(self._spriteWidgets) >= 3:
            self._spriteWidgets[-3].hide()
            self._upSprites.setEnabled(True)
            self._showSpritesWidgetIndex += 1
        return sprite

    def addSpriteWithValues(self, num, filePath):
        sprite = self.addSprite()
        sprite.setNum(num)
        sprite.setFilePath(filePath)

    def removeSprite(self, spriteWidget):
        spriteWidget.hide()
        self._spriteWidgets.remove(spriteWidget)
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
        self._fpsTE.setText(str(SettingsWidget.DEFAULT_FPS))
        self._heightTE.setText(str(SettingsWidget.DEFAULT_HEIGHT))
        self._widthTE.setText(str(SettingsWidget.DEFAULT_WIDTH))

    def getFPS(self):
        try:
            return int(self._fpsTE.text())
        except ValueError:
            return SettingsWidget.DEFAULT_FPS

    def setFPS(self, fps):
        self._fpsTE.setText(str(fps))

    def getWidth(self):
        try:
            return int(self._widthTE.text())
        except ValueError:
            return SettingsWidget.DEFAULT_WIDTH

    def setWidth(self, width):
        self._widthTE.setText(str(width))

    def getHeight(self):
        try:
            return int(self._heightTE.text())
        except ValueError:
            return SettingsWidget.DEFAULT_HEIGHT

    def setHeight(self, height):
        self._heightTE.setText(str(height))

    def getSpritesRegistery(self):
        try:
            reg = {}
            for sprW in self._spriteWidgets:
                reg[int(sprW.getNum())] = str(sprW.getFilePath())
            return reg
        except ValueError:
            return


class SpriteWidget(QWidget):
    def __init__(self, parent=None):
        super(SpriteWidget, self).__init__(parent)

        hboxToken = QHBoxLayout()
        self._previousID = None
        self._spriteIDTE = QLineEdit('Sprite ID')
        self._spriteIDTE.setMinimumHeight(30)
        self._spriteIDTE.setMaximumHeight(30)
        self._spriteFilePathTE = QLineEdit('Sprite File Path')
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
        self._spriteIDTE.textChanged.connect(self.window().setModified)
        self._spriteFilePathTE.textChanged.connect(self.window().setModified)

    def getNum(self):
        return self._spriteIDTE.text()

    def setNum(self, num):
        self._spriteIDTE.setText(str(num))

    def getFilePath(self):
        return self._spriteFilePathTE.text()

    def setFilePath(self, path):
        self._spriteFilePathTE.setText(str(path))

    def setText(self, text):
        #return self._qte.setText(text)
        pass

    def remove(self):
        self.parent().removeSprite(self)