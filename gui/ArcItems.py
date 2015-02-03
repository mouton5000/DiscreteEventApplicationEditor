# -*- coding: utf-8 -*-

__author__ = 'mouton'

from PyQt4 import QtCore
from PyQt4.QtGui import QGraphicsPathItem, QBrush, QPainterPath
from visual import vector
from math import pi, cos, degrees, atan
from random import uniform
from undoRedoActions import *
from NodeItems import NodeItem
from gui.LabelItems import LabelItem


class ArcItem(QGraphicsPathItem):
    """
    Attributs

    arrowAlpha : Demi-Largeur angulaire des arcs aux extremites
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

        self._isMoving = False
        self._moveFromCl = None

        self._separatingInput = None
        self._separatingOutput = None

        self._label = 'false'
        self._formula = 'false'
        self._consequences = []

        self._labelItem = None

    def getIndex(self):
        return self.node1.outputArcs.index(self)

    def getMaxIndex(self):
        return len(self.node1.outputArcs)

    def setIndex(self, i):
        arcs = self.node1.outputArcs
        arcs.remove(self)
        arcs.insert(i, self)
        self.node1.reorganizeArcLabels()

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label
        self.setLabelItemText(self.getIndex(), label)

    def getLabelItem(self):
        if self._labelItem is None:
            self.setLabelItem(LabelItem(scene=self.scene()))
        return self._labelItem

    def setLabelItem(self, labelItem):
        self._labelItem = labelItem
        self._labelItem.setText(str(len(self.node1.outputArcs) - 1) + ' : ' + self._label)
        self._labelItem.setBrush(QBrush(QtCore.Qt.black))
        self._labelItem.setAttachedItem(self)

    def setLabelItemText(self, index, label):
        if label:
            self._labelItem.setText(str(index) + ' : ' + label)
        else:
            self._labelItem.setText(str(index))

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
            if consequences == '':
                self._consequences = []
            else:
                self._consequences = consequences.split('\n')  # consequences is a string
        except AttributeError:
            self._consequences = consequences  # consequences is a list

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

    def changeNode(self, inputNotOutput, node):
        if inputNotOutput:
            self.node1.outputArcs.remove(self)
            self.node1.reorganizeArcLabels()
            self.node1 = node
            self.node1.outputArcs.append(self)
            self.setLabelItemText(len(self.node1.outputArcs) - 1, self.getLabel())
        else:
            self.node2.inputArcs.remove(self)
            self.node2 = node
            self.node2.inputArcs.append(self)
        self.drawPath()

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._isMoving:
            self.scene().mainWindow.stack.push(MoveArcCommand(self.scene(), self, self._moveFromCl, self._cl))
            self._isMoving = False
        elif self._separatingInput is not None:
            x, y = self._separatingInput.x, self._separatingInput.y
            n1 = self.scene().getCloseNodeOf(x, y)
            if n1 != self.node1 and n1 != self.node2:
                if n1 is None:
                    n1 = self.scene().addNode(self._separatingInput.x, self._separatingInput.y)
                self.scene().mainWindow.stack.push(ChangeInputOrOuputCommand(self.scene(), self, True, self.node1, n1))
                self._separatingInput = None
            else:
                self._separatingInput = None
                self.drawPath()
        elif self._separatingOutput is not None:
            x, y = self._separatingOutput.x, self._separatingOutput.y
            n2 = self.scene().getCloseNodeOf(x, y)
            if n2 != self.node1 and n2 != self.node2:
                if n2 is None:
                    n2 = self.scene().addNode(self._separatingOutput.x, self._separatingOutput.y)
                self.scene().mainWindow.stack.push(ChangeInputOrOuputCommand(self.scene(), self, False, self.node2, n2))
                self._separatingOutput = None
            else:
                self._separatingOutput = None
                self.drawPath()
        self.ungrabMouse()

    def mouseMoveEvent(self, event):
        if self.scene().isArcMode():
            self.moveArcEvent(event)
        elif self.scene().isSeparateInputMode():
            self.separateInputArcEvent(event)
        elif self.scene().isSeparateOutputMode():
            self.separateOutputArcEvent(event)

    def moveArcEvent(self, event):
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

    def separateInputArcEvent(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()
        node = self.scene().getCloseNodeOf(x, y)
        if node is None:
            self._separatingInput = vector(x, y)
        else:
            self._separatingInput = node.getXY()
        self.drawPath()

    def separateOutputArcEvent(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()
        node = self.scene().getCloseNodeOf(x, y)
        if node is None:
            self._separatingOutput = vector(x, y)
        else:
            self._separatingOutput = node.getXY()
        self.drawPath()

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
        self.node1.reorganizeArcLabels()
        self.node2.inputArcs.remove(self)
        self.scene().removeItem(self._labelItem)

    def getConnectedComponent(self):
        return self.node1.getConnectedComponent()

    def __str__(self):
        return str(self.node1) + ' ' + str(self.node2)

    def __repr__(self):
        return str(self.node1) + ' ' + str(self.node2)

    def drawPath(self):
        """
        Trace d'un arc reliant les noeuds node1 et node2 dans le plan.
        Attention, puisque dans le plan de l'interface, l'axe des ordonnees est invere,
        mais pas l'axe des abscisses la rotation dans le sens trigonometrique et le sens horaire sont inverses.
        """

        # Il est conseille de prendre une feuille est un stylo pour dessiner en lisant les commentaires
        # de cette methode

        if self._separatingInput is None:
            v1 = self.node1.getXY()
        else:
            v1 = self._separatingInput
        if self._separatingOutput is None:
            v2 = self.node2.getXY()
        else:
            v2 = self._separatingOutput

        u = v2 - v1  # Vecteur reliant v1 à v2
        n = (u.rotate(pi / 2)).norm()  # Vecteur unitaire perpendiculaire à u

        # Point sur la mediatrice de [v1,v2] situe a une distance cl
        # Il servira (presque) de point de controle pour les courbes de Beziers traçant les deux bords de l'arc.
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

        w = (m1p - m1m).mag / 2  # eviron la demi largeur de l'arc
        c1 = c - w * n  # point  de contrôle de la courbe de bézier du bord gauche de l'arc
        c2 = c + w * n  # point  de contrôle de la courbe de bézier du bord droit de l'arc

        # Tracé de l'arc
        path = QPainterPath()
        if self._separatingInput is not None:
            path.moveTo(v1.x + NodeItem.NodeWidth, v1.y)
            path.arcTo(v1.x - NodeItem.NodeWidth, v1.y - NodeItem.NodeWidth,
                           2 * NodeItem.NodeWidth, 2 * NodeItem.NodeWidth, 0, 360)
        path.moveTo(m1m.x, m1m.y)
        path.quadTo(c1.x, c1.y, m2pp.x, m2pp.y)
        path.lineTo(m2mp.x, m2mp.y)
        path.quadTo(c2.x, c2.y, m1p.x, m1p.y)
        path.closeSubpath()
        path.moveTo(m2.x, m2.y)
        path.lineTo(a2p.x, a2p.y)
        path.lineTo(a2m.x, a2m.y)
        path.closeSubpath()
        if self._separatingOutput is not None:
            path.moveTo(v2.x + NodeItem.NodeWidth, v2.y)
            path.arcTo(v2.x - NodeItem.NodeWidth, v2.y - NodeItem.NodeWidth,
                           2 * NodeItem.NodeWidth, 2 * NodeItem.NodeWidth, 0, 360)
        self.setPath(path)

        textCenter = v1 + u / 2 + (0.5 * self._cl) * n  # position normale
        labelItem = self.getLabelItem()
        labelItem.setCenter(textCenter)
        labelItem.setOffset(10 * w * n)  # position du texte déplacé


class CycleArcItem(ArcItem):
    def __init__(self, node1, parent=None, scene=None):
        self._delta = 0
        self._moveFromDelta = None
        super(CycleArcItem, self).__init__(node1, node1, parent, scene)

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
            self.scene().mainWindow.stack.push(MoveArcCommand(self.scene(), self, self._moveFromCl, self._cl,
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
        u = vector(1, 0).rotate(self._delta)  # vecteur normé orienté du centre du noeud vers le milieu de l'arc
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

        textCenter = o  # v1 + self._cl * u
        labelItem = self.getLabelItem()
        labelItem.setCenter(textCenter)