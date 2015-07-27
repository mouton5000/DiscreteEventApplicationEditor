__author__ = 'mouton'

DEFAULT_WIDTH = 2
DEFAULT_COLOR = '000000'

_linesList = []


def init():
    reinit()


def reinit():
    del _linesList[:]


def lineItemsIterator():
    return iter(_linesList)


class LineReg:

    def __init__(self, x1, y1, x2, y2, width, colorName):
        self.reload(x1, y1, x2, y2, width, colorName)
        _linesList.append(self)

    def reload(self, x1, y1, x2, y2, width, colorName):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.colorName = colorName

    def __str__(self):
        return str((self.x1, self.y1, self.x2, self.y2, self.width, self.colorName))

    def __repr__(self):
        return str((self.x1, self.y1, self.x2, self.y2, self.width, self.colorName))

    def remove(self):
        _linesList.remove(self)