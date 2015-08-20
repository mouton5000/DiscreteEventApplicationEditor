__author__ = 'mouton'

from collections import defaultdict
import pygame
from pygame import Color
from pygame.rect import Rect

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_ovalsList = defaultdict(list)
_rectsToUpdate = []


def init():
        reinit()


def reinit():
    _ovalsList.clear()
    del _rectsToUpdate[:]


def getLayers():
    return iter(_ovalsList.keys())


def draw(z, scene):
    for ovalItem in _ovalsList[z]:
        color = Color('#' + ovalItem.colorName)
        pygame.draw.ellipse(scene, color, Rect(ovalItem.x - ovalItem.w / 2, ovalItem.y - ovalItem.h / 2,
                                                     ovalItem.w, ovalItem.h), ovalItem.width)


def addRectToUpdate(rectToUpdate):
    _rectsToUpdate.append(rectToUpdate)


def getRectsToUpdate():
    return _rectsToUpdate


def clearRectsToUpdate():
    del _rectsToUpdate[:]


class OvalReg:

    def __init__(self, x, y, w, h, z, width, colorName):
        self.z = None
        self.x = None
        self.reload(x, y, w, h, z, width, colorName)

    def reload(self, x, y, w, h, z, width, colorName):
        if self.x is not None:
            rectToUpdate = Rect(self.x - self.w / 2 - 1, self.y - self.h / 2 - 1, self.w + 2, self.h + 2)
            r2 = Rect(x - w / 2 - 1, y - h / 2 - 1, w + 2, h + 2)
            rectToUpdate.union_ip(r2)
            addRectToUpdate(rectToUpdate)
        else:
            rectToUpdate = Rect(x - w / 2 - 1, y - h / 2 - 1, w + 2, h + 2)
            addRectToUpdate(rectToUpdate)

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = width
        self.colorName = colorName
        if self.z is not None:
            self.remove()
        _ovalsList[z].append(self)
        self.z = z

    def __str__(self):
        return str((self.x, self.y, self.h, self.w, self.width, self.colorName))

    def __repr__(self):
        return str((self.x, self.y, self.h, self.w, self.width, self.colorName))

    def remove(self):
        _ovalsList[self.z].remove(self)
        rectToUpdate = Rect(self.x - self.w / 2 - 1, self.y - self.h / 2 - 1, self.w + 2, self.h + 2)
        addRectToUpdate(rectToUpdate)