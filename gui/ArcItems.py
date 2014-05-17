__author__ = 'mouton'
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtCore import QPointF
from PyQt4.QtGui import QGraphicsSimpleTextItem, QGraphicsPathItem, QBrush, QPainterPath
from visual import vector
from math import pi, cos, degrees, atan
from random import uniform
from undoRedoActions import *
from NodeItems import NodeItem


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

        self._label = 'false'
        self._formula = 'false'
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
        for j, arc in enumerate(arcs):
            arc._setLabelItemText(j, arc._label)

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
            if consequences == '':
                self._consequences = []
            else:
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