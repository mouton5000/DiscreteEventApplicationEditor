__author__ = 'mouton'

from pygame.sprite import Sprite
import pygame
from pygame import Color
from database import UNDEFINED_PARAMETER


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