from PyQt4 import QtCore
from PyQt4.QtGui import QTabWidget, QTabBar, QWidget, QLineEdit
from SettingsItems import SettingsWidget
from gui.EditorItem import ViewWidget

__author__ = 'mouton'


class TabbedEditor(QTabWidget):
    def __init__(self, propertiesEditor, parent=None, mainWindow=None, nodesIdsGenerator=None,
                 modeController=None):
        super(TabbedEditor, self).__init__(parent)
        self.mainWindow = mainWindow
        self.setTabBar(EditableTabBar(self))
        self.setTabsClosable(True)
        self.nodesIdsGenerator = nodesIdsGenerator
        self.modeController = modeController

        self.propertiesEditor = propertiesEditor
        self.reinit()

        self.insertTabbedView()

        self.currentChanged.connect(self.tabCliked)
        self.tabCloseRequested.connect(self.closeTabbedView)

    def reinit(self):
        self.locked = True
        self.clear()

        self.addTab(QWidget(), '+')
        plusTabCLoseButton = self.tabBar().tabButton(0, QTabBar.RightSide)
        plusTabCLoseButton.resize(0, 0)
        plusTabCLoseButton.hide()

        self.settings = SettingsWidget(parent=self.mainWindow, mainWindow=self.mainWindow)
        self.insertTab(0, self.settings, 'Settings')
        settingTabCLoseButton = self.tabBar().tabButton(0, QTabBar.RightSide)
        settingTabCLoseButton.resize(0, 0)
        settingTabCLoseButton.hide()

        self.setCurrentIndex(0)

        self.locked = False

    def scenes(self):
        return (self.widget(index).scene() for index in xrange(1, self.count() - 1))

    def insertTabbedView(self, name='unnamed'):
        index = self.count() - 1
        view = ViewWidget(mainWindow=self.mainWindow, nodesIdsGenerator=self.nodesIdsGenerator,
                          modeController=self.modeController, tabIndex=index)
        view.setPropertiesEditor(self.propertiesEditor)
        self.insertTab(index, view, name)
        self.setCurrentIndex(index)
        self.setSceneName(index, name)
        return view

    def closeTabbedView(self, index):
        if index == self.count() - 2:
            self.setCurrentIndex(index - 1)
        self.removeTab(index)

    def tabCliked(self, index):
        if not self.locked and index == self.count() - 1:
            self.insertTabbedView()
        elif index > 0:
            self.widget(index).scene().reinitSelectedProperties()

    def setSceneName(self, index, name):
        self.widget(index).scene().setName(name)
        self.mainWindow.setModified()

    def settingsWidget(self):
        return self.settings


class EditableTabBar(QTabBar):
    def __init__(self, parent):
        super(EditableTabBar, self).__init__(parent)
        self._editor = QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)

    def eventFilter(self, widget, event):
        if ((event.type() == QtCore.QEvent.MouseButtonPress and
             not self._editor.geometry().contains(event.globalPos())) or
            (event.type() == QtCore.QEvent.KeyPress and
             event.key() == QtCore.Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QTabBar.eventFilter(self, widget, event)

    def mouseDoubleClickEvent(self, event):
        index = self.tabAt(event.pos())
        if 0 < index < self.count() - 1:
            self.editTab(index)

    def editTab(self, index):
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    def handleEditingFinished(self):
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            name = self._editor.text()
            self.setTabText(index, name)
            self.parent().setSceneName(index, name)

 # def __init__(self, parent=None):
 #        super(MainWidget, self).__init__(parent)
 #
 #        vbox = QVBoxLayout()
 #        self.drawing = ViewWidget(parent=self, mainWindow=self.parent())
 #        self.propertiesEditor = PropertyWidget(self)
 #        self.drawing.setPropertiesEditor(self.propertiesEditor)
 #        vbox.addWidget(self.drawing)
 #        vbox.addWidget(self.propertiesEditor)
 #        self.setLayout(vbox)
 #
 #
