__author__ = 'mouton'

from database import UNDEFINED_PARAMETER

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_rectRegs = {}


def init():
        reinit()


def reinit():
    _rectRegs.clear()


def rectItemsIterator():
    return _rectRegs.itervalues()


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


def addRect(name, x, y, w, h, width, colorName):
    _rectRegs[name] = RectReg(x, y, w, h, width, colorName)


def removeRect(name):
    try:
        del _rectRegs[name]
    except KeyError:
        pass


def editRect(name, unevaluatedX, unevaluatedY, unevaluatedW, unevaluatedH,
             unevaluatedWidth, unevaluatedColorName, evaluation):
    try:
        rect = _rectRegs[name]
    except KeyError:
        return

    newX = unevaluatedX.value(evaluation, selfParam=rect.x)
    if newX == UNDEFINED_PARAMETER:
        newX = rect.x
    else:
        newX = int(newX)

    newY = unevaluatedY.value(evaluation, selfParam=rect.y)
    if newY == UNDEFINED_PARAMETER:
        newY = rect.y
    else:
        newY = int(newY)

    newW = unevaluatedW.value(evaluation, selfParam=rect.w)
    if newW == UNDEFINED_PARAMETER:
        newW = rect.w
    else:
        newW = int(newW)

    newH = unevaluatedH.value(evaluation, selfParam=rect.h)
    if newH == UNDEFINED_PARAMETER:
        newH = rect.h
    else:
        newH = int(newH)

    newWidth = unevaluatedWidth.value(evaluation, selfParam=rect.width)
    if newWidth == UNDEFINED_PARAMETER:
        newWidth = rect.width
    else:
        newWidth = int(newWidth)

    newColorName = unevaluatedColorName.value(evaluation, selfParam=rect.colorName)
    if newColorName == UNDEFINED_PARAMETER:
        newColorName = rect.colorName
    else:
        newColorName = str(newColorName)

    rect.reload(newX, newY, newW, newH, newWidth, newColorName)