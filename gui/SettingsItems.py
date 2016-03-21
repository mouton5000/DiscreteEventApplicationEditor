__author__ = 'mouton'

from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QTextEdit


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

        self._initConsequencesTE = QTextEdit(self)
        self._initConsequencesTE.setUndoRedoEnabled(True)

        vbox.addWidget(self._initConsequencesTE)

        self.init()

        self._fpsTE.textChanged.connect(self.window().setModified)
        self._maxTickTE.textChanged.connect(self.window().setModified)
        self._widthTE.textChanged.connect(self.window().setModified)
        self._heightTE.textChanged.connect(self.window().setModified)
        self._initConsequencesTE.textChanged.connect(self.window().setModified)

        self.setLayout(vbox)

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

    def setInitConsequences(self, consequences):
        consequencesStr = ';'.join(consequences) + ';'
        self._initConsequencesTE.setText(consequencesStr)

    def getInitConsequences(self):
        consequencesStr = str(self._initConsequencesTE.toPlainText()).strip()
        if consequencesStr == '':
            return []
        else:
            consequences = consequencesStr.split(';')
            if consequences[-1] == '':
                del consequences[-1]
            return consequences