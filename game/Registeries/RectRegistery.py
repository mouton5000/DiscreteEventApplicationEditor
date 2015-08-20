__author__ = 'mouton'

from collections import defaultdict
import pygame
from pygame import Color
from pygame.rect import Rect

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_rectsList = defaultdict(list)
_rectsToUpdate = []


def init():
    reinit()


def reinit():
    _rectsList.clear()
    del _rectsToUpdate[:]


def getLayers():
    return iter(_rectsList.keys())


def draw(z, scene):
    for rectItem in _rectsList[z]:
        color = Color('#' + rectItem.colorName)
        pygame.draw.rect(scene, color, Rect(rectItem.x, rectItem.y, rectItem.w, rectItem.h), rectItem.width)


def addRectToUpdate(rectToUpdate):
    _rectsToUpdate.append(rectToUpdate)


def getRectsToUpdate():
    return _rectsToUpdate


def clearRectsToUpdate():
    del _rectsToUpdate[:]


class RectReg:

    def __init__(self, x, y, w, h, z, width, colorName):
        self.z = None
        self.x = None
        self.reload(x, y, w, h, z, width, colorName)

    def reload(self, x, y, w, h, z, width, colorName):

        if self.x is not None:
            rectToUpdate = Rect(x - 1, y - 1, w + 2, h + 2)
            r2 = Rect(self.x - 1, self.y - 1, self.w + 2, self.h + 2)
            rectToUpdate.union_ip(r2)
            addRectToUpdate(rectToUpdate)
        else:
            rectToUpdate = Rect(x - 1, y - 1, w + 2, h + 2)
            addRectToUpdate(rectToUpdate)

        self.x = x
        self.y = y
        if self.z is not None:
            self.remove()
        _rectsList[z].append(self)

        self.z = z
        self.w = w
        self.h = h
        self.width = width
        self.colorName = colorName


    def __str__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))

    def __repr__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))

    def remove(self):
        _rectsList[self.z].remove(self)
        rectToUpdate = Rect(self.x - 1, self.y - 1, self.w + 2, self.h + 2)
        addRectToUpdate(rectToUpdate)