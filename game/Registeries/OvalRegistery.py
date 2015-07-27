__author__ = 'mouton'

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_ovalsList = []


def init():
        reinit()


def reinit():
    del _ovalsList[:]


def ovalItemsIterator():
    return iter(_ovalsList)


class OvalReg:

    def __init__(self, x, y, w, h, width, colorName):
        self.reload(x, y, w, h, width, colorName)
        _ovalsList.append(self)

    def reload(self, x, y, w, h, width, colorName):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = width
        self.colorName = colorName

    def __str__(self):
        return str((self.x, self.y, self.h, self.w, self.width, self.colorName))

    def __repr__(self):
        return str((self.x, self.y, self.h, self.w, self.width, self.colorName))

    def remove(self):
        _ovalsList.remove(self)