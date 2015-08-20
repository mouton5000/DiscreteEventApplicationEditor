__author__ = 'mouton'

from collections import defaultdict
import pygame
from pygame import Color
from pygame.rect import Rect

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_polygonsList = defaultdict(list)
_rectsToUpdate = []


def init():
        reinit()


def reinit():
    _polygonsList.clear()
    del _rectsToUpdate[:]


def getLayers():
    return iter(_polygonsList.keys())


def draw(z, scene):
    for polygonItem in _polygonsList[z]:
        color = Color('#' + polygonItem.colorName)
        pygame.draw.polygon(scene, color, polygonItem.pointList, polygonItem.width)


def addRectToUpdate(rectToUpdate):
    _rectsToUpdate.append(rectToUpdate)


def getRectsToUpdate():
    return _rectsToUpdate


def clearRectsToUpdate():
    del _rectsToUpdate[:]


class PolygonReg:

    def __init__(self, pointList, z, width, colorName):
        self.z = None
        self.pointList = None
        self.reload(pointList, z, width, colorName)

    def reload(self, pointList, z, width, colorName):

        if self.pointList is not None:
            minx = min(min(x for (x, _) in pointList), min(x for (x, _) in self.pointList))
            miny = min(min(y for (_, y) in pointList), min(y for (_, y) in self.pointList))
            maxx = max(max(x for (x, _) in pointList), max(x for (x, _) in self.pointList))
            maxy = max(max(y for (_, y) in pointList), max(y for (_, y) in self.pointList))
            rectToUpdate = Rect(minx - 1, miny - 1, maxx - minx + 2, maxy - miny + 2)
            addRectToUpdate(rectToUpdate)
        else:
            minx = min(x for (x, _) in pointList)
            miny = min(y for (_, y) in pointList)
            maxx = max(x for (x, _) in pointList)
            maxy = max(y for (_, y) in pointList)
            rectToUpdate = Rect(minx - 1, miny - 1, maxx - minx + 2, maxy - miny + 2)
            addRectToUpdate(rectToUpdate)

        self.colorName = colorName
        self.pointList = pointList
        self.width = width
        if self.z is not None:
            self.remove()
        _polygonsList[z].append(self)
        self.z = z

    def __str__(self):
        return str((self.pointList, self.width, self.colorName))

    def __repr__(self):
        return str(self)

    def remove(self):
        _polygonsList[self.z].remove(self)
        minx = min(x for (x, _) in self.pointList)
        miny = min(y for (_, y) in self.pointList)
        maxx = max(x for (x, _) in self.pointList)
        maxy = max(y for (_, y) in self.pointList)
        rectToUpdate = Rect(minx - 1, miny - 1, maxx - minx + 2, maxy - miny + 2)
        addRectToUpdate(rectToUpdate)