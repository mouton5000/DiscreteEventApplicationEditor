__author__ = 'mouton'

from database import UNDEFINED_PARAMETER


_lineRegs = {}


def init():
    _lineRegs.clear()


def lineItemsIterator():
    return _lineRegs.itervalues()


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


def addLine(name, x1, y1, x2, y2, width, colorName):
    _lineRegs[name] = LineReg(x1, y1, x2, y2, width, colorName)


def removeLine(name):
    try:
        del _lineRegs[name]
    except KeyError:
        pass


def editLine(name, unevaluatedX1, unevaluatedY1, unevaluatedX2, unevaluatedY2,
             unevaluatedWidth, unevaluatedColorName, evaluation):
    try:
        line = _lineRegs[name]
    except KeyError:
        return

    newX1 = unevaluatedX1.value(evaluation, selfParam=line.x1)
    if newX1 == UNDEFINED_PARAMETER:
        newX1 = line.x1
    else:
        newX1 = int(newX1)

    newY1 = unevaluatedY1.value(evaluation, selfParam=line.y1)
    if newY1 == UNDEFINED_PARAMETER:
        newY1 = line.y1
    else:
        newY1 = int(newY1)

    newX2 = unevaluatedX2.value(evaluation, selfParam=line.x2)
    if newX2 == UNDEFINED_PARAMETER:
        newX2 = line.x2
    else:
        newX2 = int(newX2)

    newY2 = unevaluatedY2.value(evaluation, selfParam=line.y2)
    if newY2 == UNDEFINED_PARAMETER:
        newY2 = line.y2
    else:
        newY2 = int(newY2)

    newWidth = unevaluatedWidth.value(evaluation, selfParam=line.width)
    if newWidth == UNDEFINED_PARAMETER:
        newWidth = line.width
    else:
        newWidth = int(newWidth)

    newColorName = unevaluatedColorName.value(evaluation, selfParam=line.colorName)
    if newColorName == UNDEFINED_PARAMETER:
        newColorName = line.colorName
    else:
        newColorName = str(newColorName)

    line.reload(newX1, newY1, newX2, newY2, newWidth, newColorName)


