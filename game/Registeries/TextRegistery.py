__author__ = 'mouton'

import pygame
from pygame import Color


DEFAULT_COLOR = '000000'
DEFAULT_FONT_NAME = 'Arial'
DEFAULT_FONT_SIZE = 40


_textsList = []


def init():
    reinit()


def reinit():
    del _textsList[:]


def textItemsIterator():
    return iter(_textsList)


class TextReg:

    def __init__(self, text, x, y, colorName, fontName, fontSize):
        self.reload(text, x, y, colorName, fontName, fontSize)
        _textsList.append(self)

    def reload(self, text, x, y, colorName, fontName, fontSize):
        self.text = text
        self.x = x
        self.y = y
        self.colorName = colorName
        self.fontName = fontName
        self.fontSize = fontSize
        labelFont = pygame.font.SysFont(fontName, fontSize)
        self.label = labelFont.render(text, True, Color('#' + self.colorName))

    def __str__(self):
        return str((id(self), self.text, self.x, self.y, self.colorName, self.fontName, self.fontSize))

    def __repr__(self):
        return str(self)

    def remove(self):
        _textsList.remove(self)