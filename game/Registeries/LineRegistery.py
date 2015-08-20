from pygame.rect import Rect

__author__ = 'mouton'

from collections import defaultdict
import pygame
from pygame import Color

DEFAULT_WIDTH = 2
DEFAULT_COLOR = '000000'

_linesList = defaultdict(list)
_rectsToUpdate = []


def init():
    reinit()


def reinit():
    _linesList.clear()
    del _rectsToUpdate[:]


def getLayers():
    return iter(_linesList.keys())


def draw(z, scene):
    for lineItem in _linesList[z]:
        color = Color('#' + lineItem.colorName)
        pygame.draw.line(scene, color, (lineItem.x1, lineItem.y1), (lineItem.x2, lineItem.y2), lineItem.width)


def addRectToUpdate(rectToUpdate):
    _rectsToUpdate.append(rectToUpdate)


def getRectsToUpdate():
    return _rectsToUpdate


def clearRectsToUpdate():
    del _rectsToUpdate[:]


class LineReg:

    def __init__(self, x1, y1, x2, y2, z, width, colorName):
        self.z = None
        self.x1 = None
        self.reload(x1, y1, x2, y2, z, width, colorName)

    def reload(self, x1, y1, x2, y2, z, width, colorName):
        if self.x1 is not None:
            minx = min(x1, x2, self.x1, self.x2)
            miny = min(y1, y2, self.y1, self.y2)
            maxx = max(x1, x2, self.x1, self.x2)
            maxy = max(y1, y2, self.y1, self.y2)
            rectToUpdate = Rect(minx - 1, miny - 1, maxx - minx + 2, maxy - miny + 2)
            addRectToUpdate(rectToUpdate)
        else:
            minx = min(x1, x2)
            miny = min(y1, y2)
            maxx = max(x1, x2)
            maxy = max(y1, y2)
            rectToUpdate = Rect(minx - 1, miny - 1, maxx - minx + 2, maxy - miny + 2)
            addRectToUpdate(rectToUpdate)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.colorName = colorName
        if self.z is not None:
            self.remove()
        _linesList[z].append(self)
        self.z = z

    def __str__(self):
        return str((self.x1, self.y1, self.x2, self.y2, self.width, self.colorName))

    def __repr__(self):
        return str((self.x1, self.y1, self.x2, self.y2, self.width, self.colorName))

    def remove(self):
        _linesList[self.z].remove(self)
        minx = min(self.x1, self.x2)
        miny = min(self.y1, self.y2)
        maxx = max(self.x1, self.x2)
        maxy = max(self.y1, self.y2)
        rectToUpdate = Rect(minx - 1, miny - 1, maxx - minx + 2, maxy - miny + 2)
        addRectToUpdate(rectToUpdate)