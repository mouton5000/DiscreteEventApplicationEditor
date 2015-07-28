__author__ = 'mouton'

from collections import defaultdict
import pygame
from pygame import Color
from pygame.rect import Rect

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_ovalsList = defaultdict(list)


def init():
        reinit()


def reinit():
    _ovalsList.clear()


def getLayers():
    return iter(_ovalsList.keys())


def draw(z, scene):
    for ovalItem in _ovalsList[z]:
        color = Color('#' + ovalItem.colorName)
        pygame.draw.ellipse(scene, color, Rect(ovalItem.x - ovalItem.w / 2, ovalItem.y - ovalItem.h / 2,
                                                     ovalItem.w, ovalItem.h), ovalItem.width)


class OvalReg:

    def __init__(self, x, y, w, h, z, width, colorName):
        self.z = None
        self.reload(x, y, w, h, z, width, colorName)

    def reload(self, x, y, w, h, z, width, colorName):
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