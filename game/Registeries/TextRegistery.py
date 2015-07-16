__author__ = 'mouton'

import pygame
from pygame import Color
from database import UNDEFINED_PARAMETER


_textRegs = {}


def init():
        reinit()


def reinit():
    _textRegs.clear()


def textItemsIterator():
    return _textRegs.itervalues()


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


def addText(name, text, x, y, color, fontName, fontSize):
    _textRegs[name] = TextReg(text, x, y, color, fontName, fontSize)


def removeText(name):
    try:
        del _textRegs[name]
    except KeyError:
        pass


def editText(name, unevaluatedText, unevaluatedX, unevaluatedY, unevaluatedColorName,
             unevaluatedFontName, unevaluatedFontSize, evaluation):
    label = _textRegs[name]
    newText = unevaluatedText.value(evaluation, selfParam=label.text)
    if newText == UNDEFINED_PARAMETER:
        newText = label.text
    else:
        newText = str(newText)

    newX = unevaluatedX.value(evaluation, selfParam=label.x)
    if newX == UNDEFINED_PARAMETER:
        newX = label.x
    else:
        newX = int(newX)

    newY = unevaluatedY.value(evaluation, selfParam=label.y)
    if newY == UNDEFINED_PARAMETER:
        newY = label.y
    else:
        newY = int(newY)

    newColorName = unevaluatedColorName.value(evaluation, selfParam=label.colorName)
    if newColorName == UNDEFINED_PARAMETER:
        newColorName = label.colorName
    else:
        newColorName = str(newColorName)

    newFontName = unevaluatedFontName.value(evaluation, selfParam=label.fontName)
    if newFontName == UNDEFINED_PARAMETER:
        newFontName = label.fontName
    else:
        newFontName = str(newFontName)

    newFontSize = unevaluatedFontSize.value(evaluation, selfParam=label.fontSize)
    if newFontSize == UNDEFINED_PARAMETER:
        newFontSize = label.fontSize
    else:
        newFontSize = int(newFontSize)

    label.reload(newText, newX, newY, newColorName, newFontName, newFontSize)