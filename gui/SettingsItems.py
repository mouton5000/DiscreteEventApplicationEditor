from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QTextEdit

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

        self._spritesTE = QTextEdit(self)
        self._spritesTE.setUndoRedoEnabled(True)

        vbox.addWidget(self._spritesTE)

        self.init()

        self._fpsTE.textChanged.connect(self.window().setModified)
        self._widthTE.textChanged.connect(self.window().setModified)
        self._heightTE.textChanged.connect(self.window().setModified)
        self._spritesTE.textChanged.connect(self.window().setModified)

        self.setLayout(vbox)

    def setSprites(self, sprites):
        self._spritesTE.setText(sprites)

    def getSprites(self):
        return str(self._spritesTE.toPlainText())

    def getSpritesRegistery(self):
        reg = {}
        sprites = self.getSprites()
        if sprites != '':
            listOfSprites = sprites.split('\n')
            for sprStr in listOfSprites:
                    num, filePath = sprStr.split()
                    reg[int(num)] = str(filePath)
        return reg

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