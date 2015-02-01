__author__ = 'mouton'

from pygame.sprite import Sprite
import pygame
from pygame import Color


class SpriteReg(Sprite):

    def __init__(self, num, filePath, x, y, scene):
        Sprite.__init__(self)
        self.num = None
        self.reload(num, filePath, x, y, scene)

    def reload(self, num, filePath, x, y, scene):
        if self.num is None or self.num != num:
            self.num = num
            self.image = pygame.image.load(filePath).convert_alpha(scene)
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return str((self.num, self.rect))

    def __repr__(self):
        return str((self.num, self.rect))


class TextReg:

    def __init__(self, text, x, y, colorName, fontName, fontSize):
        self.reload(text, x, y, colorName, fontName, fontSize)

    def reload(self, text, x, y, colorName, fontName, fontSize):
        self.text = text
        self.colorName = colorName
        self.fontName = fontName
        self.fontSize = fontSize
        self.x = x
        self.y = y
        labelFont = pygame.font.SysFont(fontName, fontSize)
        self.label = labelFont.render(text, True, Color('#' + self.colorName))

    def __str__(self):
        return str((self.text, self.x, self.y, self.colorName, self.fontName, self.fontSize))

    def __repr__(self):
        return str((self.text, self.x, self.y, self.colorName, self.fontName, self.fontSize))


class LineReg:

    def __init__(self, x1, y1, x2, y2, width, colorName):
        self.reload(x1, y1, x2, y2, width, colorName)

    def reload(self, x1, y1, x2, y2, width, colorName):
        self.colorName = colorName
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width

    def __str__(self):
        return str((self.x1, self.y1, self.x2, self.y2, self.width, self.colorName))

    def __repr__(self):
        return str((self.x1, self.y1, self.x2, self.y2, self.width, self.colorName))


class RectReg:

    def __init__(self, x, y, w, h, width, colorName):
        self.reload(x, y, w, h, width, colorName)

    def reload(self, x, y, w, h, width, colorName):
        self.colorName = colorName
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = width

    def __str__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))

    def __repr__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))


class OvalReg:

    def __init__(self, x, y, a, b, width, colorName):
        self.reload(x, y, a, b, width, colorName)

    def reload(self, x, y, a, b, width, colorName):
        self.colorName = colorName
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.width = width

    def __str__(self):
        return str((self.x, self.y, self.a, self.b, self.width, self.colorName))

    def __repr__(self):
        return str((self.x, self.y, self.a, self.b, self.width, self.colorName))


class PolygonReg:

    def __init__(self, pointList, width, colorName):
        self.reload(pointList, width, colorName)

    def reload(self, pointList, width, colorName):
        self.colorName = colorName
        self.pointList = pointList
        self.width = width

    def __str__(self):
        return str((self.pointList, self.width, self.colorName))

    def __repr__(self):
        return str((self.pointList, self.width, self.colorName))