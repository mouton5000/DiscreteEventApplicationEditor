__author__ = 'mouton'

import abc
from game.Registeries import SpriteRegistery, \
    LineRegistery, RectRegistery, OvalRegistery, PolygonRegistery, \
    TextRegistery
from collections import defaultdict
from grammar.Keywords import KEYWORD_ID, \
    KEYWORD_X, KEYWORD_Y, KEYWORD_X_INT, KEYWORD_Y_INT,\
    KEYWORD_H, KEYWORD_W,\
    KEYWORD_CODE, KEYWORD_COLOR, KEYWORD_WIDTH, \
    KEYWORD_TEXT, KEYWORD_FONT_NAME, KEYWORD_FONT_SIZE
from itertools import count, takewhile


class UndefinedParameter:
    def __init__(self):
        pass

UNDEFINED_PARAMETER = UndefinedParameter()


def reinit():
    Property.properties.clear()
    Event.events.clear()
    SpriteProperty.sprites.clear()
    TextProperty.texts.clear()
    LineProperty.lines.clear()
    OvalProperty.ovals.clear()
    RectProperty.rects.clear()
    PolygonProperty.polygons.clear()
    NamedExpression.namedExpressionsById.clear()
    NamedExpression.expressionIDCounter = 0


class ParameterizedExpression(object):
    def __init__(self, args, kwargs):
        self._args = list(args)
        self._kwargs = kwargs

    def __str__(self):
        la = len(self._args)
        lka = len(self._kwargs)
        s = '('
        if la > 0:
            s += ', '.join([str(o) for o in self._args])
        if la > 0 and lka > 0:
            s += ','
        if lka > 0:
            s += ', '.join([str(k) + ' = ' + str(v) for k, v in self._kwargs.iteritems()])
        s += ')'
        return s

    def __repr__(self):
        return str(self)

    def update(self, args, kwargs):
        self._args = args
        self._kwargs.update(kwargs)

    def lenArgs(self):
        return len(self._args)

    def lenKWArgs(self):
        return len(self._kwargs)

    def iterArgs(self):
        return iter(self._args)

    def getArg(self, index):
        return self._args[index]

    def getKWArg(self, key):
        return self._kwargs[key]

    def setArg(self, index, value):
        self._args[index] = value

    def setKWArg(self, key, value):
        self._kwargs[key] = value

    def containsKey(self, key):
        return key in self._kwargs

    def __eq__(self, obj):
        try:
            return self._args == obj._args and self._kwargs == obj._kwargs
        except AttributeError:
            return False


class NamedExpression(ParameterizedExpression):
    __metaclass__ = abc.ABCMeta

    namedExpressionsById = dict()
    expressionIDCounter = 0

    def __init__(self, name, args, kwargs):
        super(NamedExpression, self).__init__(args, kwargs)
        self._name = name
        self._id = NamedExpression.expressionIDCounter
        NamedExpression.expressionIDCounter += 1
        NamedExpression.namedExpressionsById[self._id] = self

    @property
    def name(self):
        return self._name

    @property
    def container(self):
        return self._getContainer()

    def getKWArg(self, key):
        if key == KEYWORD_ID:
            return self._id
        else:
            return super(NamedExpression, self).getKWArg(key)

    @staticmethod
    def _addNew(cls, name, args, kwargs):
        elem = cls(name, args, kwargs)
        elem.addToContainer()

    @abc.abstractmethod
    def _getContainer(self):
        return

    def addToContainer(self):
        container = self.container
        l = container[self._name]
        try:
            l.add(self)
        except AttributeError:
            l.append(self)

    def __hash__(self):
        return hash(len(self._args) + len(self._kwargs))

    def getId(self):
        return self._id

    def filter(self, args, kwargs):
        if len(args) != self.lenArgs():
            return False

        def filterArgs(arg, propArg):
            return arg == propArg or arg == UNDEFINED_PARAMETER
        if not all(filterArgs(arg, propArg) for arg, propArg in zip(args, self.iterArgs())):
            return False

        def filterKWArgs(key, value):
            try:
                return (key == KEYWORD_ID and value == self._id) \
                    or self.getKWArg(key) == value \
                    or value == UNDEFINED_PARAMETER
            except KeyError:
                return False

        return all(filterKWArgs(key, value) for key, value in kwargs.iteritems())


    @staticmethod
    def _removeAll(name, args, kwargs, container, beforeRemove, afterRemove):
        if KEYWORD_ID in kwargs:
            elemId = kwargs[KEYWORD_ID]
            elem = NamedExpression.namedExpressionsById[elemId]
            if elem not in container[name]:
                return
            beforeRemove(elem)
            container[name].remove(elem)
            del NamedExpression.namedExpressionsById[elemId]
            afterRemove(elem)
            return

        try:
            def remove(elemToRemove):
                if elemToRemove.filter(args, kwargs):
                    beforeRemove(elemToRemove)
                    del NamedExpression.namedExpressionsById[elemToRemove.getId()]
                    afterRemove(elemToRemove)
                    return True
                return False
            typ = container.default_factory
            container[name] = typ([elem for elem in container[name]
                                             if not remove(elem)])
        except KeyError:
            pass


    @staticmethod
    def _edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation, container, beforeEdit, afterEdit):

        size = len(args1)

        print kwargs1
        if size != len(unevaluatedArgs2) and KEYWORD_ID not in kwargs1:
            return

        def editElem(elem, doFilter=True):
            if doFilter and not elem.filter(args1, kwargs1):
                return

            keys2 = [(unevaluatedKey2, unevaluatedKey2.value(evaluation)) for unevaluatedKey2 in unevaluatedKWArgs2]

            if not all(elem.containsKey(key2) for _, key2 in keys2):
                return

            newArgCommands = []
            for (index, arg), param in zip(enumerate(unevaluatedArgs2), elem.iterArgs()):
                newArg = arg.value(evaluation, selfParam=param)
                if newArg == UNDEFINED_PARAMETER:
                    newArg = param
                newArgCommands.append(newArg)

            newKWArgCommands = {}
            for unevaluatedKey2, key2 in keys2:
                unevaluatedValue2 = unevaluatedKWArgs2[unevaluatedKey2]
                value = elem.getKWArg(key2)
                value2 = unevaluatedValue2.value(evaluation, selfParam=value)
                if value2 == UNDEFINED_PARAMETER:
                    value2 = value
                newKWArgCommands[key2] = value2

            elem.update(newArgCommands, newKWArgCommands)

        if KEYWORD_ID in kwargs1:
            elem = NamedExpression.namedExpressionsById[kwargs1[KEYWORD_ID]]
            if elem not in container[name]:
                return
            beforeEdit(elem)
            editElem(elem, False)
            afterEdit(elem)
            return

        try:
            elems = container[name]
        except KeyError:
            return

        for elem in elems:
            beforeEdit(elem)
            editElem(elem)
            afterEdit(elem)


class Property(NamedExpression):
    properties = defaultdict(set)

    def __init__(self, name, args, kwargs):
        super(Property, self).__init__(name, args, kwargs)

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(Property, name, args, kwargs)

    @staticmethod
    def removeAll(name, args, kwargs):

        def beforeRemove(_):
            pass

        def afterRemove(_):
            pass

        Property._removeAll(name, args, kwargs, Property.properties, beforeRemove, afterRemove)

    @staticmethod
    def editAll(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):

        def beforeEdit(_):
            pass

        def afterEdit(_):
            pass

        Property._edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation,
                       Property.properties, beforeEdit, afterEdit)

    def _getContainer(self):
        return Property.properties


class Event(NamedExpression):
    events = defaultdict(set)

    def __init__(self, name, args, kwargs):
        super(Event, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return Event.events

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(Event, name, args, kwargs)


class SpriteProperty(NamedExpression):
    sprites = defaultdict(list)

    def __init__(self, name, args, kwargs):
        super(SpriteProperty, self).__init__(name, args, kwargs)
        self._spriteRegister = None
        self.initSpriteRegister()

    def getSpriteInfo(self):
        return \
            int(self._kwargs[KEYWORD_CODE]), \
            int(self._kwargs[KEYWORD_X]), \
            int(self._kwargs[KEYWORD_Y])

    def initSpriteRegister(self):
        code, x, y = self.getSpriteInfo()
        self._spriteRegister = SpriteRegistery.SpriteReg(code, x, y)

    def reloadSpriteRegister(self):
        code, x, y = self.getSpriteInfo()
        self._spriteRegister.reload(code, x, y)

    def getSpriteRegister(self):
        return self._spriteRegister

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(SpriteProperty, name, args, kwargs)

    @staticmethod
    def removeAll(name, args, kwargs):

        def beforeRemove(_):
            pass

        def afterRemove(sprite):
            sprite.getSpriteRegister().remove()

        SpriteProperty._removeAll(name, args, kwargs, SpriteProperty.sprites, beforeRemove, afterRemove)

    @staticmethod
    def editAll(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):

        def beforeEdit(_):
            pass

        def afterEdit(sprite):
            sprite.reloadSpriteRegister()

        SpriteProperty._edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation,
                             SpriteProperty.sprites, beforeEdit, afterEdit)

    def _getContainer(self):
        return SpriteProperty.sprites


class TextProperty(NamedExpression):
    texts = defaultdict(list)

    def __init__(self, name, args, kwargs):
        super(TextProperty, self).__init__(name, args, kwargs)
        self._textRegister = None
        self.initTextRegister()

    def getTextInfo(self):

        return \
            str(self._kwargs[KEYWORD_TEXT]), \
            int(self._kwargs[KEYWORD_X]), \
            int(self._kwargs[KEYWORD_Y]), \
            str(self._kwargs.setdefault(KEYWORD_COLOR, TextRegistery.DEFAULT_COLOR)), \
            str(self._kwargs.setdefault(KEYWORD_FONT_NAME, TextRegistery.DEFAULT_FONT_NAME)), \
            int(self._kwargs.setdefault(KEYWORD_FONT_SIZE, TextRegistery.DEFAULT_FONT_SIZE))

    def initTextRegister(self):
        text, x, y, color, fontName, fontSize = self.getTextInfo()
        self._textRegister = TextRegistery.TextReg(text, x, y, color, fontName, fontSize)

    def reloadTextRegister(self):
        text, x, y, color, fontName, fontSize = self.getTextInfo()
        self._textRegister.reload(text, x, y, color, fontName, fontSize)

    def getTextRegister(self):
        return self._textRegister

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(TextProperty, name, args, kwargs)

    @staticmethod
    def removeAll(name, args, kwargs):

        def beforeRemove(_):
            pass

        def afterRemove(text):
            text.getTextRegister().remove()

        TextProperty._removeAll(name, args, kwargs, TextProperty.texts, beforeRemove, afterRemove)

    @staticmethod
    def editAll(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):

        def beforeEdit(_):
            pass

        def afterEdit(text):
            text.reloadTextRegister()

        TextProperty._edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation,
                             TextProperty.texts, beforeEdit, afterEdit)

    def _getContainer(self):
        return TextProperty.texts


class LineProperty(NamedExpression):
    lines = defaultdict(list)

    def __init__(self, name, args, kwargs):
        super(LineProperty, self).__init__(name, args, kwargs)
        self._lineRegister = None
        self.initLineRegister()

    def getLineInfo(self):

        return \
            int(self._kwargs[KEYWORD_X_INT[1]]), \
            int(self._kwargs[KEYWORD_Y_INT[1]]), \
            int(self._kwargs[KEYWORD_X_INT[2]]), \
            int(self._kwargs[KEYWORD_Y_INT[2]]), \
            int(self._kwargs.setdefault(KEYWORD_WIDTH, LineRegistery.DEFAULT_WIDTH)), \
            str(self._kwargs.setdefault(KEYWORD_COLOR, LineRegistery.DEFAULT_COLOR))

    def initLineRegister(self):
        x1, y1, x2, y2, width, color = self.getLineInfo()
        self._lineRegister = LineRegistery.LineReg(x1, y1, x2, y2, width, color)

    def reloadLineRegister(self):
        x1, y1, x2, y2, width, color = self.getLineInfo()
        self._lineRegister.reload(x1, y1, x2, y2, width, color)

    def getLineRegister(self):
        return self._lineRegister

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(LineProperty, name, args, kwargs)

    @staticmethod
    def removeAll(name, args, kwargs):

        def beforeRemove(_):
            pass

        def afterRemove(line):
            line.getLineRegister().remove()

        LineProperty._removeAll(name, args, kwargs, LineProperty.lines, beforeRemove, afterRemove)

    @staticmethod
    def editAll(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):

        def beforeEdit(_):
            pass

        def afterEdit(line):
            line.reloadLineRegister()

        LineProperty._edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation,
                             LineProperty.lines, beforeEdit, afterEdit)

    def _getContainer(self):
        return LineProperty.lines


class OvalProperty(NamedExpression):
    ovals = defaultdict(list)

    def __init__(self, name, args, kwargs):
        super(OvalProperty, self).__init__(name, args, kwargs)
        self._ovalRegister = None
        self.initOvalRegister()

    def getOvalInfo(self):
        return \
            int(self._kwargs[KEYWORD_X]), \
            int(self._kwargs[KEYWORD_Y]), \
            int(self._kwargs[KEYWORD_W]), \
            int(self._kwargs[KEYWORD_H]), \
            int(self._kwargs.setdefault(KEYWORD_WIDTH, OvalRegistery.DEFAULT_WIDTH)), \
            str(self._kwargs.setdefault(KEYWORD_COLOR, OvalRegistery.DEFAULT_COLOR))

    def initOvalRegister(self):
        x, y, w, h, width, color = self.getOvalInfo()
        self._ovalRegister = OvalRegistery.OvalReg(x, y, h, w, width, color)

    def reloadOvalRegister(self):
        x, y, w, h, width, color = self.getOvalInfo()
        self._ovalRegister.reload(x, y, h, w, width, color)

    def getOvalRegister(self):
        return self._ovalRegister

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(OvalProperty, name, args, kwargs)

    @staticmethod
    def removeAll(name, args, kwargs):

        def beforeRemove(_):
            pass

        def afterRemove(oval):
            oval.getOvalRegister().remove()

        OvalProperty._removeAll(name, args, kwargs, OvalProperty.ovals, beforeRemove, afterRemove)

    @staticmethod
    def editAll(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):

        def beforeEdit(_):
            pass

        def afterEdit(oval):
            oval.reloadOvalRegister()

        OvalProperty._edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation,
                             OvalProperty.ovals, beforeEdit, afterEdit)

    def _getContainer(self):
        return OvalProperty.ovals


class RectProperty(NamedExpression):
    rects = defaultdict(list)

    def __init__(self, name, args, kwargs):
        super(RectProperty, self).__init__(name, args, kwargs)
        self._rectRegister = None
        self.initRectRegister()

    def getRectInfo(self):
        return \
            int(self._kwargs[KEYWORD_X]), \
            int(self._kwargs[KEYWORD_Y]), \
            int(self._kwargs[KEYWORD_W]), \
            int(self._kwargs[KEYWORD_H]), \
            int(self._kwargs.setdefault(KEYWORD_WIDTH, OvalRegistery.DEFAULT_WIDTH)), \
            str(self._kwargs.setdefault(KEYWORD_COLOR, OvalRegistery.DEFAULT_COLOR))

    def initRectRegister(self):
        x, y, w, h, width, color = self.getRectInfo()
        self._rectRegister = RectRegistery.RectReg(x, y, h, w, width, color)

    def reloadRectRegister(self):
        x, y, w, h, width, color = self.getRectInfo()
        self._rectRegister.reload(x, y, h, w, width, color)

    def getRectRegister(self):
        return self._rectRegister

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(RectProperty, name, args, kwargs)

    @staticmethod
    def removeAll(name, args, kwargs):

        def beforeRemove(_):
            pass

        def afterRemove(rect):
            rect.getRectRegister().remove()

        RectProperty._removeAll(name, args, kwargs, RectProperty.rects, beforeRemove, afterRemove)

    @staticmethod
    def editAll(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):

        def beforeEdit(_):
            pass

        def afterEdit(rect):
            rect.reloadRectRegister()

        RectProperty._edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation,
                             RectProperty.rects, beforeEdit, afterEdit)

    def _getContainer(self):
        return RectProperty.rects


class PolygonProperty(NamedExpression):
    polygons = defaultdict(list)

    def __init__(self, name, args, kwargs):
        super(PolygonProperty, self).__init__(name, args, kwargs)
        self._polygonRegister = None
        self.initPolygonRegister()

    def getPolygonInfo(self):
        def _generator():
            for index in count(1):
                yield self._kwargs.get(KEYWORD_X_INT[index]),\
                    self._kwargs.get(KEYWORD_Y_INT[index])

        def _correctValues(xy):
            x, y = xy
            return x is not None and y is not None

        points = [(int(x), int(y)) for x, y in takewhile(_correctValues, _generator())]
        return \
            points,\
            int(self._kwargs.setdefault(KEYWORD_WIDTH, PolygonRegistery.DEFAULT_WIDTH)), \
            str(self._kwargs.setdefault(KEYWORD_COLOR, PolygonRegistery.DEFAULT_COLOR))

    def initPolygonRegister(self):
        points, width, color = self.getPolygonInfo()
        self._polygonRegister = PolygonRegistery.PolygonReg(points, width, color)

    def reloadPolygonRegister(self):
        points, width, color = self.getPolygonInfo()
        self._polygonRegister.reload(points, width, color)

    def getPolygonRegister(self):
        return self._polygonRegister

    @staticmethod
    def add(name, args, kwargs):
        NamedExpression._addNew(PolygonProperty, name, args, kwargs)

    @staticmethod
    def removeAll(name, args, kwargs):

        def beforeRemove(_):
            pass

        def afterRemove(polygon):
            polygon.getPolygonRegister().remove()

        PolygonProperty._removeAll(name, args, kwargs, PolygonProperty.polygons, beforeRemove, afterRemove)

    @staticmethod
    def editAll(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):

        def beforeEdit(_):
            pass

        def afterEdit(polygon):
            polygon.reloadPolygonRegister()

        PolygonProperty._edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation,
                              PolygonProperty.polygons, beforeEdit, afterEdit)

    def _getContainer(self):
        return PolygonProperty.polygons


class Variable(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)