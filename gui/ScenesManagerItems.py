from PyQt4.QtCore import QStringList, QModelIndex, Qt
from PyQt4.QtGui import QListView, QStringListModel, QApplication, QInputDialog,\
    QAbstractItemView, QMessageBox
from gui.EditorItem import ViewWidget

__author__ = 'mouton'


class ViewsManagerWidget(QListView):
    def __init__(self, parent=None, propertiesEditor=None, mainWindow=None, nodesIdsGenerator=None,
                 modeController=None):
        super(ViewsManagerWidget, self).__init__(parent)
        self.setMaximumWidth(200)
        self._views = []
        self._viewsListModel = ViewManagerModel()
        self.setModel(self._viewsListModel)
        self.reinit()

        self.mainWindow = mainWindow
        self.nodesIdsGenerator = nodesIdsGenerator
        self.modeController = modeController

        self.propertiesEditor = propertiesEditor

        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.doubleClicked.connect(self._viewDoubleClicked)
        self.setEditTriggers(QAbstractItemView.EditKeyPressed)

    def reinit(self):
        del self._views[:]
        self._viewsListModel.setStringList(QStringList())
        self._counter = 0

    def addView(self):
        self._counter += 1
        return self.addNamedView('unnamed' + str(self._counter))

    def addNamedView(self, name):
        view = ViewWidget(mainWindow=self.mainWindow, nodesIdsGenerator=self.nodesIdsGenerator,
                          modeController=self.modeController)
        view.setPropertiesEditor(self.propertiesEditor)
        size = self._viewsListModel.rowCount()
        self._viewsListModel.insertRow(size)
        index = self._viewsListModel.index(size, 0)
        self._views.append(view)
        self._viewsListModel.setData(index, name)
        self._selectedIndex = None
        self.mainWindow.setModified()
        return view

    def removeIndex(self, indexRow):
        del self._views[indexRow]
        self._viewsListModel.removeRow(indexRow)
        self._selectedIndex = None
        self.mainWindow.setModified()

    def scenes(self):
        return (view.scene() for view in self._views)

    def _viewDoubleClicked(self, index):
        view = self._views[index.row()]
        tabItem = self.mainWindow.centralWidget().tabItem()
        tabItem.showTabbedView(view)

    def dataChanged(self, index, _):
        try:
            name = self._viewsListModel.stringList()[index.row()]
            view = self._views[index.row()]
            view.scene().setName(name)
            self.mainWindow.setModified()
        except IndexError:
            pass

    def keyPressEvent(self, event):
      if event.key() == Qt.Key_Delete:
        def row(index):
          return index.row()
        selected = sorted(self.selectedIndexes(), key=row, reverse=True)
        if len(selected) > 0:
          reply = QMessageBox.warning(self, 'Delete one or more scenes', 
                                      'Are you sure you want to delete this or these scenes? You will not be able to get access to them in the future.', 
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
          if reply == QMessageBox.Yes:
            for index in selected:
              self.removeIndex(index.row())
      else:
        super(ViewsManagerWidget, self).keyPressEvent(event)

class ViewManagerModel(QStringListModel):
    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | \
                    Qt.ItemIsDropEnabled | Qt.ItemIsEnabled
