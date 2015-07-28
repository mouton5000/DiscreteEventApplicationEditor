__author__ = 'mouton'

from collections import defaultdict
import pygame
from pygame import Color
from pygame.rect import Rect

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_rectsList = defaultdict(list)


def init():
        reinit()


def reinit():
    _rectsList.clear()


def getLayers():
    return iter(_rectsList.keys())


def draw(z, scene):
    for rectItem in _rectsList[z]:
        color = Color('#' + rectItem.colorName)
        pygame.draw.rect(scene, color, Rect(rectItem.x, rectItem.y, rectItem.w, rectItem.h), rectItem.width)


class RectReg:

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
        _rectsList[z].append(self)
        self.z = z

    def __str__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))

    def __repr__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))

    def remove(self):
        _rectsList[self.z].remove(self)