__author__ = 'mouton'

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_polygonsList = []


def init():
        reinit()


def reinit():
    del _polygonsList[:]


def polygonItemsIterator():
    return iter(_polygonsList)


class PolygonReg:

    def __init__(self, pointList, width, colorName):
        self.reload(pointList, width, colorName)
        _polygonsList.append(self)

    def reload(self, pointList, width, colorName):
        self.colorName = colorName
        self.pointList = pointList
        self.width = width

    def __str__(self):
        return str((self.pointList, self.width, self.colorName))

    def __repr__(self):
        return str(self)

    def remove(self):
        _polygonsList.remove(self)