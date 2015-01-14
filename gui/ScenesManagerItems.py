from PyQt4.QtCore import QStringList, QModelIndex, Qt, QString
from PyQt4.QtGui import QListView, QStringListModel, QApplication, QInputDialog,\
    QAbstractItemView, QMessageBox, QListWidget, QListWidgetItem
from gui.EditorItem import ViewWidget

__author__ = 'mouton'


from PyQt4.QtCore import QStringList, QModelIndex, Qt
from PyQt4.QtGui import QListView, QStringListModel, QApplication, QInputDialog,\
    QAbstractItemView, QMessageBox
from gui.EditorItem import ViewWidget

__author__ = 'mouton'


class ViewsManagerWidget(QListWidget):
    def __init__(self, parent=None, propertiesEditor=None, mainWindow=None, nodesIdsGenerator=None,
                 modeController=None):
        super(ViewsManagerWidget, self).__init__(parent)
        self.setMaximumWidth(200)
        self.reinit()

        self.mainWindow = mainWindow
        self.nodesIdsGenerator = nodesIdsGenerator
        self.modeController = modeController

        self.propertiesEditor = propertiesEditor

        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setEditTriggers(QAbstractItemView.EditKeyPressed)

        self.itemDoubleClicked.connect(self._viewDoubleClicked)
        self.itemChanged.connect(self._itemEdited)

        # self..connect(self._test)

    def reinit(self):
        self._counter = 0
        self.clear()

    def addView(self):
        self._counter += 1
        return self.addNamedView('unnamed' + str(self._counter))

    def addNamedView(self, name):
        view = ViewWidget(mainWindow=self.mainWindow, nodesIdsGenerator=self.nodesIdsGenerator,
                          modeController=self.modeController)
        view.setPropertiesEditor(self.propertiesEditor)

        item = ViewsManagerItem(view)
        item.setText(name)
        self.addItem(item)
        item.reloadViewName()
        self.mainWindow.setModified()
        return view

    def scenes(self):
        return (self.item(index).view.scene() for index in xrange(self.count()))

    def _viewDoubleClicked(self, item):
        view = item.view
        tabItem = self.mainWindow.centralWidget().tabItem()
        tabItem.showTabbedView(view)

    def _itemEdited(self, item):
        item.reloadViewName()
        self.mainWindow.setModified()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            def row(index):
                return index.row()
            selected = sorted(self.selectedIndexes(), key=row, reverse=True)
            if len(selected) > 0:
                reply = QMessageBox.warning(self, 'Delete one or more scenes',
                                            'Are you sure you want to delete this or these scenes? \
                                            You will not be able to get access to them in the future.',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    for index in selected:
                        self.takeItem(index.row())
                    self.mainWindow.setModified()
        else:
            super(ViewsManagerWidget, self).keyPressEvent(event)

    def dropEvent(self, event):
        self.mainWindow.setModified()
        super(ViewsManagerWidget, self).dropEvent(event)


class ViewsManagerItem(QListWidgetItem):
    def __init__(self, view, parent=None):
        super(ViewsManagerItem, self).__init__(parent)
        self.view = view
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.reloadViewName()

    def reloadViewName(self):
        name = self.text()
        self.view.scene().setName(name)