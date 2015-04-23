__author__ = 'mouton'

from database import UNDEFINED_PARAMETER


_ovalRegs = {}


def init():
    _ovalRegs.clear()


def ovalItemsIterator():
    return _ovalRegs.itervalues()


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


def addOval(name, x, y, a, b, width, colorName):
    _ovalRegs[name] = OvalReg(x, y, a, b, width, colorName)


def removeOval(name):
    try:
        del _ovalRegs[name]
    except KeyError:
        pass


def editOval(name, unevaluatedX, unevaluatedY, unevaluatedA, unevaluatedB,
             unevaluatedWidth, unevaluatedColorName, evaluation):
    try:
        oval = _ovalRegs[name]
    except KeyError:
        return

    newX = unevaluatedX.value(evaluation, selfParam=oval.x)
    if newX == UNDEFINED_PARAMETER:
        newX = oval.x
    else:
        newX = int(newX)

    newY = unevaluatedY.value(evaluation, selfParam=oval.y)
    if newY == UNDEFINED_PARAMETER:
        newY = oval.y
    else:
        newY = int(newY)

    newA = unevaluatedA.value(evaluation, selfParam=oval.a)
    if newA == UNDEFINED_PARAMETER:
        newA = oval.a
    else:
        newA = int(newA)

    newB = unevaluatedB.value(evaluation, selfParam=oval.b)
    if newB == UNDEFINED_PARAMETER:
        newB = oval.b
    else:
        newB = int(newB)

    newWidth = unevaluatedWidth.value(evaluation, selfParam=oval.width)
    if newWidth == UNDEFINED_PARAMETER:
        newWidth = oval.width
    else:
        newWidth = int(newWidth)

    newColorName = unevaluatedColorName.value(evaluation, selfParam=oval.colorName)
    if newColorName == UNDEFINED_PARAMETER:
        newColorName = oval.colorName
    else:
        newColorName = str(newColorName)

    oval.reload(newX, newY, newA, newB, newWidth, newColorName)