#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore

from PyQt4.QtCore import QRectF, QPointF
from PyQt4.QtGui import QApplication as QApp, QVBoxLayout, QHBoxLayout, QTextEdit, QGraphicsSimpleTextItem, QAction, \
    QFileDialog, QMainWindow, QWidget, QDesktopWidget, QLabel, QComboBox, QGraphicsView, QGraphicsScene, \
    QGraphicsEllipseItem, QGraphicsPathItem, QBrush, QPainterPath, QUndoStack
from visual import vector
from math import pi, cos, degrees, atan
from random import uniform
from copy import copy

import json

from undoRedoActions import *

import os.path


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        self.stack = QUndoStack()

        self._lastSaveOpenFileDirectory = '/home'

    def init_ui(self):
        widget = MainWidget(self)
        self.setCentralWidget(widget)
        self.initMenu()

        self.setGeometry(0, 0, 800, 640)
        self.setWindowTitle('GraphEditor')
        self.center()
        self.show()

    def initMenu(self):
        newAction = QAction('&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.new)

        saveAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)

        loadAction = QAction('&Load', self)
        loadAction.setShortcut('Ctrl+O')
        loadAction.triggered.connect(self.load)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)

        undoAction = QAction('&Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.triggered.connect(self.undo)

        redoAction = QAction('&Redo', self)
        redoAction.setShortcut('Ctrl+Shift+Z')
        redoAction.triggered.connect(self.redo)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)

    def scene(self):
        return self.centralWidget().drawing.scene()

    def new(self):
        scene = self.scene()
        scene.clear()
        return scene

    def save(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Choose save destination', self._lastSaveOpenFileDirectory)
            with open(fname, 'w') as f:
                scene = self.scene()
                nodes = scene.nodes

                def nodeDict(node):
                    d = dict()
                    xy = node.getXY()
                    d['x'], d['y'] = xy.x, xy.y
                    d['isActive'] = node.isActive()
                    return d

                def arcDict(arc):
                    d = dict()
                    d['n1'] = nodes.index(arc.node1)
                    d['n2'] = nodes.index(arc.node2)
                    d['cl'] = arc.getCl()
                    try:
                        d['delta'] = arc.getDelta()
                    except AttributeError:
                        pass
                    d['label'] = arc.getLabel()
                    d['formula'] = arc.getFormula()
                    d['consequences'] = arc.getConsequences()
                    offset = arc.getLabelItem().getOffset()
                    d['labelItemOffset'] = [offset.x, offset.y]
                    return d

                from itertools import chain

                d = {
                    "nodes": [nodeDict(node) for node in nodes],
                    "arcs": [arcDict(arc) for arc in chain.from_iterable(node.outputArcs for node in nodes)]}
                json.dump(d, f)

                self._lastSaveOpenFileDirectory = os.path.dirname(str(fname))
        except IOError:
            pass

    def load(self):
        scene = self.new()

        try:
            fname = QFileDialog.getOpenFileName(self, 'Choose file to open', self._lastSaveOpenFileDirectory)

            with open(fname) as f:
                d = json.load(f)

                def addNode(node):
                    x = node['x']
                    y = node['y']
                    n = scene.addNode(x, y)
                    n.setActive(node['isActive'])
                    return n

                nodes = [addNode(node) for node in d['nodes']]

                def addArc(arc):
                    n1 = nodes[arc['n1']]
                    n2 = nodes[arc['n2']]
                    a = scene.addArc(n1, n2)
                    if n1 == n2:
                        a.setClAndDelta(arc['cl'], arc['delta'])
                    else:
                        a.setCl(arc['cl'])
                    a.setLabel(arc['label'])
                    a.setFormula(arc['formula'])
                    a.setConsequences(arc['consequences'])
                    lioff = arc['labelItemOffset']
                    a.getLabelItem().setOffset(vector(lioff[0], lioff[1]))

                for arc in d['arcs']:
                    addArc(arc)

                self._lastSaveOpenFileDirectory = os.path.dirname(str(fname))
        except IOError:
            pass

    def undo(self):
        self.stack.undo()

    def redo(self):
        self.stack.redo()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        pass

        # reply = QMB.question(self, 'Message', 'Quit?', QMB.Yes | QMB.No, QMB.No)
        #
        # if reply == QMB.Yes:
        #     event.accept()
        # else:
        #     event.ignore()


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        vbox = QVBoxLayout()
        self.drawing = ViewWidget(self)
        self.params = ArcParamEditorWidget(self)
        self.drawing.setArcParamEditor(self.params)
        vbox.addWidget(self.drawing)
        vbox.addWidget(self.params)
        self.setLayout(vbox)


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

        self.setMaximumHeight(200)

    def init(self):
        self._indexQCB.clear()
        self.setLabel('Etiquette de l\'arc.')
        self.setFormula('Formule d\'acceptance de l\'arc.')
        self.setConsequences('Consequences du passage par l\'arc.')

    def setIndexes(self, maxIndex, index):
        self._indexQCB.clear()
        for i in range(maxIndex):
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


class ViewWidget(QGraphicsView):
    def __init__(self, parent=None):
        super(ViewWidget, self).__init__(parent)
        scene = SceneWidget(self)
        self.setScene(scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rect = QRectF(-200, -200, 400, 400)
        self.setSceneRect(self.rect)
        self.px = None
        self.py = None
        self.arcParamEditor = None

    def mouseMoveEvent(self, event):
        item = self.scene().mouseGrabberItem()
        if item:
            super(ViewWidget, self).mouseMoveEvent(event)
        else:
            x, y = event.x(), event.y()
            if self.px:
                self.translate(x - self.px, y - self.py)
            self.px = x
            self.py = y

    def mouseReleaseEvent(self, event):
        if self.px:
            self.px = None
            self.py = None
        else:
            super(ViewWidget, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        dx, dy = 0, 0
        if event.key() == QtCore.Qt.Key_Right:
            dx, dy = 30, 0
        elif event.key() == QtCore.Qt.Key_Left:
            dx, dy = -30, 0
        elif event.key() == QtCore.Qt.Key_Up:
            dx, dy = 0, -30
        elif event.key() == QtCore.Qt.Key_Down:
            dx, dy = 0, 30
        else:
            super(ViewWidget, self).keyPressEvent(event)
        if dx != 0 or dy != 0:
            self.translate(dx, dy)

    def translate(self, dx, dy):
        self.rect.translate(-dx, -dy)
        self.setSceneRect(self.rect)

    def setArcParamEditor(self, ape):
        self.arcParamEditor = ape


class SceneWidget(QGraphicsScene):
    NodeMode = 0
    PathMode = 1
    StarMode = 2

    def __init__(self, parent=None):
        super(SceneWidget, self).__init__(parent)
        self.init()

    def init(self):
        self.nodes = []
        self._nodeId = 0
        self._selected = None
        self._mode = None
        self.setNodeMode()

    def addItem(self, item):
        super(SceneWidget, self).addItem(item)
        try:
            item.add()
        except AttributeError:
            pass

    def clear(self):
        super(SceneWidget, self).clear()
        self.init()

    def addNode(self, x, y):
        node = NodeItem(x, y, self._nodeId, scene=self)
        self._nodeId += 1
        self.setSelected(node)
        # Apparently, addItem is not called when an item is created
        node.add()
        return node

    def addArc(self, n1, n2):
        if n1 == n2:
            arc = CycleArcItem(n1, scene=self)
        else:
            arc = ArcItem(n1, n2, scene=self)
        if self.isPathMode():
            self.setSelected(n2)
        return arc

    def mouseReleaseEvent(self, event):
        item = self.mouseGrabberItem()
        if self.isNodeMode():
            if not item:
                x, y = event.scenePos().x(), event.scenePos().y()
                self.addNode(x, y)
            elif isinstance(item, NodeItem):
                self.setSelected(item)
                item.mouseReleaseEvent(event)
            else:
                item.mouseReleaseEvent(event)
        elif self.isArcMode():
            if not item:
                self.setSelected(None)
            else:
                if isinstance(item, NodeItem):
                    if isinstance(self._selected, NodeItem):
                        self.addArc(self._selected, item)
                    else:
                        self.setSelected(item)
                else:
                    self.setSelected(item)
                item.mouseReleaseEvent(event)

    def setSelected(self, item):
        if self._selected == item:
            return
        if self._selected:
            try:
                self._selected.unselect()
            except AttributeError:
                pass
        self._selected = item
        if item:
            try:
                item.select()
            except AttributeError:
                pass
        self.parent().arcParamEditor.setSelectedArc(item)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_N:
            self.setNodeMode()
        elif event.key() == QtCore.Qt.Key_P:
            self.setPathMode()
        elif event.key() == QtCore.Qt.Key_S:
            self.setStarMode()
        elif event.key() == QtCore.Qt.Key_Delete:
            if self._selected:
                self.deleteSelected()
        else:
            item = self.mouseGrabberItem()
            try:
                item.keyReleaseEvent(event)
            except AttributeError:
                pass

    def setNodeMode(self):
        self.setMode(SceneWidget.NodeMode)
        self.parent().parent().parent().statusBar().showMessage('Node mode')
        if isinstance(self._selected, ArcItem):
            self.setSelected(None)

    def setPathMode(self):
        self.setMode(SceneWidget.PathMode)
        self.parent().parent().parent().statusBar().showMessage('Path mode')

    def setStarMode(self):
        self.setMode(SceneWidget.StarMode)
        self.parent().parent().parent().statusBar().showMessage('Star mode')

    def setMode(self, mode):
        self._mode = mode

    def isNodeMode(self):
        return self._mode == SceneWidget.NodeMode

    def isArcMode(self):
        return self.isPathMode() or self.isStarMode()

    def isPathMode(self):
        return self._mode == SceneWidget.PathMode

    def isStarMode(self):
        return self._mode == SceneWidget.StarMode

    def deleteSelected(self):
        self.parent().window().stack.push(DeleteItemCommand(self, self._selected))
        self.setSelected(None)

    def deleteItem(self, item):
        item.remove()
        self.removeItem(item)


class NodeItem(QGraphicsEllipseItem):
    NodeWidth = 20

    def __init__(self, x, y, num, parent=None, scene=None):
        super(NodeItem, self).__init__(x - NodeItem.NodeWidth, y - NodeItem.NodeWidth, NodeItem.NodeWidth * 2,
                                       NodeItem.NodeWidth * 2, parent, scene)
        self._num = num
        self._center = vector(x, y)
        self.outputArcs = []
        self.inputArcs = []

        self._isMoving = False
        self._moveFrom = None

        self.scene().parent().window().stack.push(AddItemCommand(self.scene(), self))

        self._isActive = False
        self.setBrush(QBrush(QtCore.Qt.black))

    def add(self):
        self.scene().nodes.append(self)

    def mouseDoubleClickEvent(self, QGraphicsSceneMouseEvent):
        if self.scene().isNodeMode():
            self.scene().parent().window().stack.push(SetActiveNodeCommand(self, not self._isActive))

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.scene().parent().window().stack.push(MoveNodeCommand(self, self._moveFrom, self._center))
            self._moveFromX = None
            self._moveFromY = None
            self._isMoving = False
        self.ungrabMouse()

    def select(self):
        br = self.brush()
        br.setStyle(QtCore.Qt.Dense3Pattern)
        self.setBrush(br)

    def unselect(self):
        br = self.brush()
        br.setStyle(QtCore.Qt.SolidPattern)
        self.setBrush(br)

    def setActive(self, isActive):
        self._isActive = isActive
        br = self.brush()
        if isActive:
            br.setColor(QtCore.Qt.red)
        else:
            br.setColor(QtCore.Qt.black)
        self.setBrush(br)

    def isActive(self):
        return self._isActive

    def mouseMoveEvent(self, event):
        if not self.scene().isNodeMode():
            return

        if not self._isMoving:
            self._isMoving = True
            self._moveFrom = self._center

        x = event.scenePos().x()
        y = event.scenePos().y()
        self.setXY(x, y)

    def setXY(self, x, y):
        dx, dy = x - self._center.x, y - self._center.y
        self.moveBy(dx, dy)
        self._center = vector(x, y)

        for a in self.inputArcs:
            a.drawPath()

        for a in self.outputArcs:
            a.drawPath()

    def getXY(self):
        return self._center

    def isPredecessorOf(self, node):
        for a in self.outputArcs:
            if a.node2 == node:
                return True
        return False

    def isSuccessorOf(self, node):
        for a in self.inputArcs:
            if a.node1 == node:
                return True
        return False

    def remove(self):
        self.scene().nodes.remove(self)
        for a in copy(self.inputArcs):
            self.scene().parent().window().stack.push(DeleteItemCommand(self.scene(), a))
        for a in copy(self.outputArcs):
            self.scene().parent().window().stack.push(DeleteItemCommand(self.scene(), a))

    def __str__(self):
        return str(self._num)

    def __repr__(self):
        return str(self._num)


class ArcItem(QGraphicsPathItem):
    """

    Attributs

    arrowAlpha : Demi-Largeur angulaire des arcs aux extrêmités
    arrowBeta : Demi angle de la pointe de l'arc
    """

    endingsAlpha = pi / 12
    arrowBeta = pi / 4

    def __init__(self, node1, node2, parent=None, scene=None):
        super(ArcItem, self).__init__(parent, scene)

        self.node1 = node1
        self.node2 = node2

        self.setBrush(QBrush(QtCore.Qt.black))

        self._cl = 0
        self.initPath()

        node1.outputArcs.append(self)
        node2.inputArcs.append(self)

        self._isMoving = False
        self._moveFromCl = None

        self.scene().parent().window().stack.push(AddItemCommand(self.scene(), self))

        self._label = 'False'
        self._formula = 'False'
        self._consequences = []

        self._labelItem = ArcLabelItem(str(len(node1.outputArcs) - 1) + ' : ' + self._label,
                                       parent=self, scene=self.scene())
        self._labelItem.setBrush(QBrush(QtCore.Qt.black))

        self.drawPath()

    def getIndex(self):
        return self.node1.outputArcs.index(self)

    def getMaxIndex(self):
        return len(self.node1.outputArcs)

    def setIndex(self, i):
        arcs = self.node1.outputArcs
        arcs.remove(self)
        arcs.insert(i, self)
        for j in range(len(arcs)):
            arcs[j]._setLabelItemText(j, arcs[j]._label)

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label
        self._setLabelItemText(self.getIndex(), label)

    def _setLabelItemText(self, index, label):
        self._labelItem.setText(str(index) + ' : ' + label)

    def getFormula(self):
        return self._formula

    def setFormula(self, formula):
        self._formula = formula

    def getConsequences(self):
        return self._consequences

    def getConsequencesStr(self):
        return '\n'.join(self._consequences)

    def setConsequences(self, consequences):
        try:
            self._consequences = consequences.split('\n')  # consequences is a string
        except AttributeError:
            self._consequences = consequences  # consequences is a list

    def getLabelItem(self):
        return self._labelItem

    def initPath(self):
        cls = []
        for a in self.node1.outputArcs:
            if a.node2 == self.node2:
                cls.append((int(a._cl) + 30) / 60)
        cl = 0
        b = True
        while cl / 60 in cls:
            if b:
                cl *= -1
                cl += 60
            else:
                cl *= -1
            b = not b
        self._cl = cl

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.scene().parent().window().stack.push(MoveArcCommand(self, self._moveFromCl, self._cl))
            self._isMoving = False
        self.ungrabMouse()

    def mouseMoveEvent(self, event):
        if not self.scene().isArcMode():
            return

        if not self._isMoving:
            self._isMoving = True
            self._moveFromCl = self._cl

        x = event.scenePos().x()
        y = event.scenePos().y()
        v1 = self.node1.getXY()
        v2 = self.node2.getXY()
        v = vector(x, y) - v1
        u = v2 - v1
        n = (u.rotate(pi / 2)).norm()

        self.setCl((2 * v).dot(n))

    def getCl(self):
        return self._cl

    def setCl(self, cl):
        self._cl = cl
        self.drawPath()

    def select(self):
        br = self.brush()
        br.setStyle(QtCore.Qt.Dense3Pattern)
        self.setBrush(br)

    def unselect(self):
        br = self.brush()
        br.setStyle(QtCore.Qt.SolidPattern)
        self.setBrush(br)

    def remove(self):
        self.node1.outputArcs.remove(self)
        self.node2.inputArcs.remove(self)

    def __str__(self):
        return str(self.node1) + ' ' + str(self.node2)

    def __repr__(self):
        return str(self.node1) + ' ' + str(self.node2)

    def drawPath(self):
        """
        Tracé d'un arc reliant les noeuds node1 et node2 dans le plan.
        Attention, puisque dans le plan de l'interface, l'axe des ordonnées est inveré,
        mais pas l'axe des abscisses la rotation dans le sens trigonométrique et le sens horaire sont inversés.
        """

        # Il est conseillé de prendre une feuille est un stylo pour dessiner en lisant les commentaires
        # de cette méthode

        v1 = self.node1.getXY()
        v2 = self.node2.getXY()

        u = v2 - v1  # Vecteur reliant v1 à v2
        n = (u.rotate(pi / 2)).norm()  # Vecteur unitaire perpendiculaire à u

        # Point sur la médiatrice de [v1,v2] situé à une distance cl
        # Il servira (presque) de point de contrôle pour les courbes de Beziers traçant les deux bords de l'arc.
        c = v1 + u / 2 + self._cl * n

        v1m1norm = (c - v1).norm()  # Vecteur unitaire de la droite (v1,c), de v1 vers c
        v2m2norm = (c - v2).norm()  # Vecteur unitaire de la droite (v2,c), de v2 vers c

        # m1 est le point du cercle node1 situé sur la droite (v1,c) entre ces deux points.
        # c'est également le milieu du départ de l'arc sur node1
        v1m1 = NodeItem.NodeWidth * v1m1norm  # Vecteur v1m1
        # Point sur le cercle node1 à une distance angulaire -alpha de m1
        m1m = v1 + v1m1.rotate(-ArcItem.endingsAlpha)
        # Point sur le cercle node1 à une distance angulaire alpha de m1
        m1p = v1 + v1m1.rotate(ArcItem.endingsAlpha)

        # m2 est le point du cercle node2 situé sur la droite (v2,c) entre ces deux points.
        # c'est également la pointe de la flêche de l'arc
        v2m2 = NodeItem.NodeWidth * v2m2norm  # Vecteur v2m2
        m2 = v2 + v2m2  # Point m2
        a2 = v2 + 2 * v2m2  # a2 est le milieu du segment central de la pointe de la flêche de l'arc
        # a2m est l'extrêmité droite de la pointe de la flêche
        a2m = v2 + v2m2 + (NodeItem.NodeWidth / cos(ArcItem.arrowBeta)) * v2m2norm.rotate(-ArcItem.arrowBeta)
        # a2p est l'extrêmité gauche de la pointe de la flêche
        a2p = v2 + v2m2 + (NodeItem.NodeWidth / cos(ArcItem.arrowBeta)) * v2m2norm.rotate(ArcItem.arrowBeta)
        # m2m est le point sur le cercle node2 à une distance angulaire -alpha de m2
        v2m2m = v2m2.rotate(-ArcItem.endingsAlpha)  # Vecteur v2 m2m
        # m2p est le point sur le cercle node2 à une distance angulaire alpha de m2
        v2m2p = v2m2.rotate(ArcItem.endingsAlpha)  # Vecteur v2 m2p
        # m2mp est le point sur le segment central de la pointe de la flêche qui appartient à la droite passant
        # par m2m parallèle au vecteur v2m2, définit ici à l'aide d'un projeté orthogonal
        m2mp = a2 + v2m2m.proj(a2m - a2)
        # m2pp est le point sur le segment central de la pointe de la flêche qui appartient à la droite passant
        # par m2p parallèle au vecteur v2m2, définit ici à l'aide d'un projeté orthogonal
        m2pp = a2 + v2m2p.proj(a2p - a2)

        w = (m1p - m1m).mag / 2 # eviron la demi largeur de l'arc
        c1 = c - w * n  # point  de contrôle de la courbe de bézier du bord gauche de l'arc
        c2 = c + w * n  # point  de contrôle de la courbe de bézier du bord droit de l'arc

        # Tracé de l'arc
        path = QPainterPath()
        path.moveTo(m1m.x, m1m.y)
        path.quadTo(c1.x, c1.y, m2pp.x, m2pp.y)
        path.lineTo(m2mp.x, m2mp.y)
        path.quadTo(c2.x, c2.y, m1p.x, m1p.y)
        path.closeSubpath()
        path.moveTo(m2.x, m2.y)
        path.lineTo(a2p.x, a2p.y)
        path.lineTo(a2m.x, a2m.y)
        path.closeSubpath()
        self.setPath(path)

        textCenter = v1 + u / 2 + (0.5 * self._cl) * n  # position normale
        textPos = textCenter + 10 * w * n + self._labelItem.getOffset()  # position du texte déplacé
        self._labelItem.setCenter(textCenter)
        self._labelItem.setPos(textPos.x, textPos.y)


class CycleArcItem(ArcItem):
    def __init__(self, node1, parent=None, scene=None):
        self._delta = 0
        self._moveFromDelta = None
        super(CycleArcItem, self).__init__(node1, node1, parent, scene)
        self.drawPath()

    def initPath(self):
        self._delta = uniform(0, 2 * pi)
        self._cl = 100

    def getDelta(self):
        return self._delta

    def setClAndDelta(self, cl, delta):
        self._delta = delta
        self.setCl(cl)

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.scene().parent().window().stack.push(MoveArcCommand(self, self._moveFromCl, self._cl,
                                                                     self._moveFromDelta, self._delta))
            self._isMoving = False
        self.ungrabMouse()

    def mouseMoveEvent(self, event):
        if not self.scene().isArcMode():
            return

        if not self._isMoving:
            self._isMoving = True
            self._moveFromCl = self._cl
            self._moveFromDelta = self._delta

        x = event.scenePos().x()
        y = event.scenePos().y()
        v1 = self.node1.getXY()
        v = vector(x, y) - v1
        cl = v.mag
        if cl < 50:
            cl = 50

        sindelta = vector(0, 1).dot(v) / cl
        delta = vector(1, 0).diff_angle(v)
        if sindelta < 0:
            delta *= -1
        self.setClAndDelta(cl, delta)

    def drawPath(self):
        """
        Tracé d'un arc reliant le noeud node1 à lui même dans le plan.
        Attention, puisque dans le plan de l'interface, l'axe des ordonnées est inveré,
        mais pas l'axe des abscisses la rotation dans le sens trigonométrique et le sens horaire sont inversés.
        """

        # Il est conseillé de prendre une feuille est un stylo pour dessiner en lisant les commentaires
        # de cette méthode

        v1 = v2 = self.node1.getXY()

        # m1 et o sont des points définis plus loin, mais on peut calculer et on a besoin de calculer leur distance
        # dès maintenant
        m1omag = float(self._cl ** 2 - NodeItem.NodeWidth ** 2) / (2 * self._cl)

        # demi angle entre les tangentes de l'arc à ses deux extrêmités (entre l'arrivée et le départ).
        gamma = atan(m1omag / NodeItem.NodeWidth)

        # delta est l'angle qui existe entre l'horizontale est la droite coupant orthogonalement l'arc en son milieu
        u = vector(1, 0).rotate(self._delta) # vecteur normé orienté du centre du noeud vers le milieu de l'arc
        # m1 est le point du cercle node1 au milieu du départ de l'arc
        v1m1norm = (u.rotate(-gamma))
        # m2 est la pointe de la flêche de l'arc
        v2m2norm = (u.rotate(gamma))

        v1m1 = NodeItem.NodeWidth * v1m1norm
        # Point sur le cercle node1 à une distance angulaire -alpha de m1
        m1m = v1 + v1m1.rotate(-ArcItem.endingsAlpha)
        # Point sur le cercle node1 à une distance angulaire alpha de m1
        m1p = v1 + v1m1.rotate(ArcItem.endingsAlpha)

        v2m2 = NodeItem.NodeWidth * v2m2norm
        m2 = v2 + v2m2  # Point m2
        a2 = v2 + 2 * v2m2  # a2 est le milieu du segment central de la pointe de la flêche de l'arc
        # a2m est l'extrêmité droite de la pointe de la flêche
        a2m = v2 + v2m2 + (NodeItem.NodeWidth / cos(ArcItem.arrowBeta)) * v2m2norm.rotate(-ArcItem.arrowBeta)
        # a2p est l'extrêmité gauche de la pointe de la flêche
        a2p = v2 + v2m2 + (NodeItem.NodeWidth / cos(ArcItem.arrowBeta)) * v2m2norm.rotate(ArcItem.arrowBeta)
        # m2m est le point sur le cercle node2 à une distance angulaire -alpha de m2
        v2m2m = v2m2.rotate(-ArcItem.endingsAlpha)  # Vecteur v2 m2m
        # m2p est le point sur le cercle node2 à une distance angulaire alpha de m2
        v2m2p = v2m2.rotate(ArcItem.endingsAlpha)  # Vecteur v2 m2p
        # m2mp est le point sur le segment central de la pointe de la flêche qui appartient à la droite passant
        # par m2m parallèle au vecteur v2m2, définit ici à l'aide d'un projeté orthogonal
        m2mp = a2 + v2m2m.proj(a2m - a2)
        # m2pp est le point sur le segment central de la pointe de la flêche qui appartient à la droite passant
        # par m2p parallèle au vecteur v2m2, définit ici à l'aide d'un projeté orthogonal
        m2pp = a2 + v2m2p.proj(a2p - a2)

        # o est le centre du cercle passant par les 3 points suivants : m1, m2 et c
        # où c est le point situé à une distance self.cl de v1, en suivant le vecteur u, cad le milieu de l'arc
        o = v1 + v1m1 + m1omag * v1m1norm.rotate(pi / 2)

        c1 = 0.5 * (m2pp + m1m)  # c1 est le milieu de m2pp et m1m
        # o1 est le centre du cercle passant par m1m et m2pp le plus proche de o
        o1 = c1 + (o - c1).proj((m1m - m2pp).rotate(pi / 2))
        r1 = (o1 - m1m).mag  # le rayon du cercle en question

        sinstang1 = vector(0, 1).dot(m1m - o1)  # sinus de l'angle entre l'horizontale et (o1,m1m)
        stang1 = -vector(1, 0).diff_angle(m1m - o1)  # opposé de la valeur absolue de cet angle
        if sinstang1 < 0:
            stang1 *= -1
        sinendang1 = vector(0, 1).dot(m2pp - o1)  # sinus de l'angle entre l'horizontale et (o1,m2pp)
        endang1 = -vector(1, 0).diff_angle(m2pp - o1)  # opposé de la valeur absolue de cet angle
        if sinendang1 < 0:
            endang1 *= -1
        pathang1 = endang1 - stang1
        while pathang1 > 0:  # correctifs pour afficher un bel arc de cercle dans le bon sens
            pathang1 -= 2 * pi
        while pathang1 < -2 * pi:
            pathang1 += 2 * pi

        c2 = 0.5 * (m2mp + m1p)  # c2 est le milieu de m2mp et m1p
        # o2 est le centre du cercle passant par m1p et m2mp le plus proche de o
        o2 = c2 + (o - c2).proj((m1p - m2mp).rotate(pi / 2))
        r2 = (o2 - m1p).mag  # le rayon du cercle en question
        sinstang2 = vector(0, 1).dot(m2mp - o2)  # sinus de l'angle entre l'horizontale et (o2,m2mp)
        stang2 = -vector(1, 0).diff_angle(m2mp - o2)  # opposé de la valeur absolue de cet angle
        if sinstang2 < 0:
            stang2 *= -1
        sinendang2 = vector(0, 1).dot(m1p - o2)  # sinus de l'angle entre l'horizontale et (o2,m1p)
        endang2 = -vector(1, 0).diff_angle(m1p - o2)  # opposé de la valeur absolue de cet angle
        if sinendang2 < 0:
            endang2 *= -1
        pathang2 = endang2 - stang2
        while pathang2 > 2 * pi:  # correctifs pour afficher un bel arc de cercle dans le bon sens
            pathang2 -= 2 * pi
        while pathang2 < 0:
            pathang2 += 2 * pi


        # Tracé du chemin
        path = QPainterPath()
        path.moveTo(m1m.x, m1m.y)
        path.arcTo(o1.x - r1, o1.y - r1, 2 * r1, 2 * r1, degrees(stang1), degrees(pathang1))
        path.lineTo(m2pp.x, m2pp.y)
        path.lineTo(m2mp.x, m2mp.y)
        path.arcTo(o2.x - r2, o2.y - r2, 2 * r2, 2 * r2, degrees(stang2), degrees(pathang2))
        path.lineTo(m1p.x, m1p.y)
        path.closeSubpath()
        path.moveTo(m2.x, m2.y)
        path.lineTo(a2p.x, a2p.y)
        path.lineTo(a2m.x, a2m.y)
        path.closeSubpath()
        self.setPath(path)

        textCenter = v1 + self._cl * u
        textPos = o + self._labelItem.getOffset()  # position du texte
        self._labelItem.setCenter(textCenter)
        self._labelItem.setPos(textPos.x, textPos.y)


class ArcLabelItem(QGraphicsSimpleTextItem):
    def __init__(self, text, parent=None, scene=None):
        super(ArcLabelItem, self).__init__(text, parent, scene)
        self._offset = vector(0, 0)
        self._center = vector(0, 0)
        self._isMoving = False
        self._moveFromOffset = False

        self._linkToArc = self.scene().addLine(0, 0, 0, 0)
        self._linkToArc.setVisible(False)

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.scene().parent().window().stack.push(MoveArcLabelCommand(self, self._moveFromOffset, self._offset))
            self._isMoving = False
            self._linkToArc.setVisible(False)
        self.ungrabMouse()

    def mouseMoveEvent(self, event):
        if not self._isMoving:
            self._isMoving = True
            self._moveFromOffset = self._offset
            self._linkToArc.setVisible(True)

        epos = vector(event.scenePos().x(), event.scenePos().y())
        rect = self.boundingRect()
        pos = vector(self.pos().x() + rect.width() / 2, self.pos().y() + rect.height() / 2)
        center = pos - self._offset
        self.setOffset(epos - center)

        line = self._linkToArc.line()
        line.setP2(QPointF(self.pos().x() + rect.width() / 2, self.pos().y() + rect.height()))
        self._linkToArc.setLine(line)

    def setCenter(self, center):
        self._center = center
        line = self._linkToArc.line()
        line.setP1(QPointF(center.x, center.y))
        self._linkToArc.setLine(line)

    def setOffset(self, offset):
        dpos = offset - self._offset
        self.moveBy(dpos.x, dpos.y)
        self._offset = offset

    def getOffset(self):
        return self._offset


def main():
    app = QApp(sys.argv)
    ex = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



