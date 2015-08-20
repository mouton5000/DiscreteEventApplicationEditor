from pygame.rect import Rect

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
_rectsToUpdate = []


def init(rootDir):
    global _rootDir
    _rootDir = rootDir
    reinit()


def reinit():
    _textsList.clear()
    del _rectsToUpdate[:]


def getLayers():
    return iter(_textsList.keys())


def draw(z, scene):
    for textItem in _textsList[z]:
        label = textItem.label
        textPos = label.get_rect()
        textPos.centerx = textItem.x
        textPos.centery = textItem.y
        scene.blit(label, textPos)


def addRectToUpdate(rectToUpdate):
    _rectsToUpdate.append(rectToUpdate)


def getRectsToUpdate():
    return _rectsToUpdate


def clearRectsToUpdate():
    del _rectsToUpdate[:]


class TextReg:

    def __init__(self, text, x, y, z, colorName, fontName, fontSize):
        self.z = None
        self.label = None
        self.x = None
        self.y = None
        self.reload(text, x, y, z, colorName, fontName, fontSize)

    def reload(self, text, x, y, z, colorName, fontName, fontSize):

        prevRect = None
        if self.label is not None:
            prevRect = self.label.get_rect()

        self.text = text
        prevX = self.x
        prevY = self.y
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

        rect = self.label.get_rect()

        if prevRect is not None:

            rectToUpdate = Rect(prevX - prevRect.width / 2 - 1, prevY - prevRect.height / 2 - 1,
                                prevRect.width + 2, prevRect.height + 2)
            r2 = Rect(x - rect.width / 2 - 1, y - rect.height / 2 - 1, rect.width + 2, rect.height + 2)
            rectToUpdate.union_ip(r2)
            addRectToUpdate(rectToUpdate)
        else:
            rectToUpdate = Rect(x - rect.width / 2 - 1, y - rect.height / 2 - 1, rect.width + 2, rect.height + 2)
            addRectToUpdate(rectToUpdate)

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
        rect = self.label.get_rect()
        rectToUpdate = Rect(self.x - rect.width / 2 - 1, self.y - rect.height / 2 - 1, rect.width + 2, rect.height + 2)
        addRectToUpdate(rectToUpdate)