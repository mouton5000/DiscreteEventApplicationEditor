__author__ = 'mouton'

from collections import defaultdict
import pygame
from pygame import Color

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_polygonsList = defaultdict(list)


def init():
        reinit()


def reinit():
    _polygonsList.clear()


def getLayers():
    return iter(_polygonsList.keys())


def draw(z, scene):
    for polygonItem in _polygonsList[z]:
        color = Color('#' + polygonItem.colorName)
        pygame.draw.polygon(scene, color, polygonItem.pointList, polygonItem.width)


class PolygonReg:

    def __init__(self, pointList, z, width, colorName):
        self.z = None
        self.reload(pointList, z, width, colorName)

    def reload(self, pointList, z, width, colorName):
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