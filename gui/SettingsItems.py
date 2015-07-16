from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QTextEdit

__author__ = 'mouton'


class SettingsWidget(QWidget):

    DEFAULT_FPS = 60
    DEFAULT_MAX_TICK = 1000
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 640

    def __init__(self, parent=None, mainWindow=None):
        super(SettingsWidget, self).__init__(parent)
        self.mainWindow = mainWindow

        vbox = QVBoxLayout()

        self._spriteWidgets = []
        self._showSpritesWidgetIndex = 0

        hboxFPSTick = QHBoxLayout()
        self._fpsTE = QLineEdit(self)
        self._maxTickTE = QLineEdit(self)
        
        hboxFPSTick.addWidget(self._fpsTE)
        hboxFPSTick.addWidget(self._maxTickTE)

        hboxSize = QHBoxLayout()
        self._widthTE = QLineEdit(self)
        self._heightTE = QLineEdit(self)

        hboxSize.addWidget(self._widthTE)
        hboxSize.addWidget(self._heightTE)

        vbox.addLayout(hboxFPSTick)
        vbox.addLayout(hboxSize)

        self._spritesTE = QTextEdit(self)
        self._spritesTE.setUndoRedoEnabled(True)

        vbox.addWidget(self._spritesTE)

        self._soundsTE = QTextEdit(self)
        self._soundsTE.setUndoRedoEnabled(True)

        vbox.addWidget(self._soundsTE)

        self.init()

        self._fpsTE.textChanged.connect(self.window().setModified)
        self._maxTickTE.textChanged.connect(self.window().setModified)
        self._widthTE.textChanged.connect(self.window().setModified)
        self._heightTE.textChanged.connect(self.window().setModified)
        self._spritesTE.textChanged.connect(self.window().setModified)
        self._soundsTE.textChanged.connect(self.window().setModified)

        self.setLayout(vbox)

    def setSprites(self, sprites):
        self._spritesTE.setText(sprites)

    def getSprites(self):
        return str(self._spritesTE.toPlainText())

    def getSpritesDictionnary(self):
        dic = {}
        sprites = self.getSprites()
        if sprites != '':
            listOfSprites = sprites.split('\n')
            for sprStr in listOfSprites:
                    num, filePath = sprStr.split()
                    dic[int(num)] = str(filePath)
        return dic

    def setSounds(self, sounds):
        self._soundsTE.setText(sounds)

    def getSounds(self):
        return str(self._soundsTE.toPlainText())

    def getSoundsDictionnary(self):
        dic = {}
        sounds = self.getSounds()
        if sounds != '':
            listOfSounds = sounds.split('\n')
            for sndStr in listOfSounds:
                    num, filePath = sndStr.split()
                    dic[int(num)] = str(filePath)
        return dic

    def init(self):
        self._fpsTE.setText(str(SettingsWidget.DEFAULT_FPS))
        self._maxTickTE.setText(str(SettingsWidget.DEFAULT_MAX_TICK))
        self._heightTE.setText(str(SettingsWidget.DEFAULT_HEIGHT))
        self._widthTE.setText(str(SettingsWidget.DEFAULT_WIDTH))

    def getFPS(self):
        try:
            return int(self._fpsTE.text())
        except ValueError:
            return SettingsWidget.DEFAULT_FPS

    def setFPS(self, fps):
        self._fpsTE.setText(str(fps))
    
    def getMaxTick(self):
        try:
            return int(self._maxTickTE.text())
        except ValueError:
            return SettingsWidget.DEFAULT_MAX_TICK

    def setMaxTick(self, maxTick):
        self._maxTickTE.setText(str(maxTick))

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
