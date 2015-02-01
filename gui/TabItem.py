from PyQt4.QtGui import QTabWidget, QTabBar
from SettingsItems import SettingsWidget

__author__ = 'mouton'


class TabbedEditor(QTabWidget):
    def __init__(self, propertiesEditor, parent=None, mainWindow=None, nodesIdsGenerator=None,
                 modeController=None):
        super(TabbedEditor, self).__init__(parent)
        self.mainWindow = mainWindow
        self.setTabsClosable(True)
        self.nodesIdsGenerator = nodesIdsGenerator
        self.modeController = modeController

        self.propertiesEditor = propertiesEditor
        self.reinit()

        self.currentChanged.connect(self.tabCliked)
        self.tabCloseRequested.connect(self.closeTabbedView)

    def reinit(self):
        self.locked = True
        self.clear()

        self.settings = SettingsWidget(parent=self.mainWindow, mainWindow=self.mainWindow)
        self.insertTab(0, self.settings, 'Settings')
        settingTabCLoseButton = self.tabBar().tabButton(0, QTabBar.RightSide)
        settingTabCLoseButton.resize(0, 0)
        settingTabCLoseButton.hide()

        self.setCurrentIndex(0)

        self.locked = False

    def scenes(self):
        return (self.widget(index).scene() for index in xrange(1, self.count()))

    def getScene(self, index):
        return self.widget(index).scene()

    def setTabbedViewText(self, view, name):
        tabIndex = self.indexOf(view)
        if tabIndex != -1:
            self.setTabText(tabIndex, name)

    def showTabbedView(self, view):
        tabIndex = self.indexOf(view)
        if tabIndex == -1:
            self.insertTabbedView(view)
        else:
            self.setCurrentIndex(tabIndex)

    def insertTabbedView(self, view):
        index = self.count()
        name = view.scene().getName()
        self.addTab(view, name)
        self.setCurrentIndex(index)
        return view

    def closeTabbedView(self, index):
        if index == self.count() - 1:
            self.setCurrentIndex(index)
        self.removeTab(index)

    def tabCliked(self, index):
        if index > 0:
            self.widget(index).scene().reinitSelectedProperties()
        else:
            self.propertiesEditor.setNoItem()

    def settingsWidget(self):
        return self.settings