__author__ = 'mouton'

import pygame
from pygame import Color
from collections import defaultdict

pygame.font.init()

DEFAULT_COLOR = '000000'
DEFAULT_FONT_NAME = 'Arial'
DEFAULT_FONT_SIZE = 40


_textsList = defaultdict(list)
_rootDir = None


def init(rootDir):
    global _rootDir
    _rootDir = rootDir
    reinit()


def reinit():
    _textsList.clear()


def getLayers():
    return iter(_textsList.keys())


def draw(z, scene):
    for textItem in _textsList[z]:
        label = textItem.label
        textPos = label.get_rect()
        textPos.centerx = textItem.x
        textPos.centery = textItem.y
        scene.blit(label, textPos)


class TextReg:

    def __init__(self, text, x, y, z, colorName, fontName, fontSize):
        self.z = None
        self.reload(text, x, y, z, colorName, fontName, fontSize)

    def reload(self, text, x, y, z, colorName, fontName, fontSize):
        self.text = text
        self.x = x
        self.y = y
        self.colorName = colorName
        fontName = _rootDir + '/' + fontName
        self.fontName = fontName
        self.fontSize = fontSize
        try:
            labelFont = pygame.font.Font(fontName, fontSize)
        except IOError:
            labelFont = pygame.font.SysFont('', fontSize)
        self.label = labelFont.render(text, True, Color('#' + self.colorName))
        if self.z is not None:
            self.remove()
        _textsList[z].append(self)
        self.z = z

    def __str__(self):
        return str((id(self), self.text, self.x, self.y, self.colorName, self.fontName, self.fontSize))

    def __repr__(self):
        return str(self)

    def remove(self):
        _textsList[self.z].remove(self)