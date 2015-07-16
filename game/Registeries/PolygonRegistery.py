__author__ = 'mouton'

from database import UNDEFINED_PARAMETER

DEFAULT_WIDTH = 1
DEFAULT_COLOR = '000000'

_polygonRegs = {}


def init():
        reinit()


def reinit():
    _polygonRegs.clear()


def polygonItemsIterator():
    return _polygonRegs.itervalues()


class PolygonReg:

    def __init__(self, pointList, width, colorName):
        self.reload(pointList, width, colorName)

    def reload(self, pointList, width, colorName):
        self.colorName = colorName
        self.pointList = pointList
        self.width = width

    def __str__(self):
        return str((self.pointList, self.width, self.colorName))

    def __repr__(self):
        return str((self.pointList, self.width, self.colorName))


def addPolygon(name, listPoint, width, colorName):
    _polygonRegs[name] = PolygonReg(listPoint, width, colorName)


def removePolygon(name):
    try:
        del _polygonRegs[name]
    except KeyError:
        pass


def editPolygon(name, unevaluatedPointList, unevaluatedWidth, unevaluatedColorName, evaluation):
    try:
        polygon = _polygonRegs[name]
    except KeyError:
        return

    minLen = min(len(unevaluatedPointList), len(polygon.pointList))

    def addPoint(i, point):
        unevaluatedPoint = unevaluatedPointList[i]

        def getPoint(j):
            if point is None:
                v = None
            else:
                v = point[j]
            newXj = unevaluatedPoint[j].value(evaluation, selfParam=v)
            if newXj == UNDEFINED_PARAMETER:
                newXj = v
            else:
                newXj = int(newXj)
            return newXj

        newPoint = [getPoint(0), getPoint(1)]
        return newPoint

    newPointList = [addPoint(k, polygon.pointList[k]) for k in xrange(minLen)]

    if minLen < len(unevaluatedPointList):
        for k in xrange(minLen, len(unevaluatedPointList)):
            newPointList.append(addPoint(k, None))

    newWidth = unevaluatedWidth.value(evaluation, selfParam=polygon.width)
    if newWidth == UNDEFINED_PARAMETER:
        newWidth = polygon.width
    else:
        newWidth = int(newWidth)

    newColorName = unevaluatedColorName.value(evaluation, selfParam=polygon.colorName)
    if newColorName == UNDEFINED_PARAMETER:
        newColorName = polygon.colorName
    else:
        newColorName = str(newColorName)

    polygon.reload(newPointList, newWidth, newColorName)