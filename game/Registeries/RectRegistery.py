__author__ = 'mouton'

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_rectsList = []


def init():
        reinit()


def reinit():
    del _rectsList[:]


def rectItemsIterator():
    return iter(_rectsList)


class RectReg:

    def __init__(self, x, y, w, h, width, colorName):
        self.reload(x, y, w, h, width, colorName)
        _rectsList.append(self)

    def reload(self, x, y, w, h, width, colorName):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = width
        self.colorName = colorName

    def __str__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))

    def __repr__(self):
        return str((self.x, self.y, self.w, self.h, self.width, self.colorName))

    def remove(self):
        _rectsList.remove(self)