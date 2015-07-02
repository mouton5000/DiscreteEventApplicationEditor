__author__ = 'mouton'

import abc


class UndefinedParameter:
    def __init__(self):
        pass

UNDEFINED_PARAMETER = UndefinedParameter()


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


class KeyWordId:
    def __init__(self):
        pass

    def value(self, _):
        return self

KEYWORD_ID = KeyWordId()


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

    @abc.abstractmethod
    def _getContainer(self):
        return

    def addToContainer(self):
        container = self.container
        try:
            l = container[self._name]
            l.add(self)
        except KeyError:
            l = set([self])
            container[self._name] = l

    def __hash__(self):
        return hash(len(self._args) + len(self._kwargs))

    def getId(self):
        return self._id


class Property(NamedExpression):
    properties = dict()

    def __init__(self, name, args, kwargs):
        super(Property, self).__init__(name, args, kwargs)

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
    def add(name, args, kwargs):
        prop = Property(name, args, kwargs)
        prop.addToContainer()

    @staticmethod
    def removeAll(name, args, kwargs):
            if KEYWORD_ID in kwargs:
                propId = kwargs[KEYWORD_ID]
                prop = NamedExpression.namedExpressionsById[propId]
                if prop.filter(args, kwargs):
                    Property.properties[name].remove(prop)
                    del NamedExpression.namedExpressionsById[propId]
            else:
                try:
                    def remove(propToRemove):
                        if propToRemove.filter(args, kwargs):
                            del NamedExpression.namedExpressionsById[propToRemove.getId()]
                            return True
                        return False
                    Property.properties[name] = set([prop for prop in Property.properties[name]
                                                     if not remove(prop)])
                except KeyError:
                    pass

    @staticmethod
    def edit(name, args1, kwargs1, unevaluatedArgs2, unevaluatedKWArgs2, evaluation):
        size = len(args1)
        if size != len(unevaluatedArgs2):
            return

        def editProp(prop):
            if not prop.filter(args1, kwargs1):
                return

            keys2 = [(unevaluatedKey2, unevaluatedKey2.value(evaluation)) for unevaluatedKey2 in unevaluatedKWArgs2]

            if not all(prop.containsKey(key2) for _, key2 in keys2):
                return

            newArgCommands = []
            for (index, arg), param in zip(enumerate(unevaluatedArgs2), prop.iterArgs()):
                newArg = arg.value(evaluation, selfParam=param)
                if newArg == UNDEFINED_PARAMETER:
                    newArg = param
                newArgCommands.append(newArg)

            newKWArgCommands = {}
            for unevaluatedKey2, key2 in keys2:
                unevaluatedValue2 = unevaluatedKWArgs2[unevaluatedKey2]
                value = prop.getKWArg(key2)
                value2 = unevaluatedValue2.value(evaluation, selfParam=value)
                if value2 == UNDEFINED_PARAMETER:
                    value2 = value
                newKWArgCommands[key2] = value2

            prop._args = newArgCommands
            prop._kwargs = newKWArgCommands

        if KEYWORD_ID in kwargs1:
            prop = NamedExpression.namedExpressionsById[kwargs1[KEYWORD_ID]]
            editProp(prop)
        else:
            try:
                props = Property.properties[name]
            except KeyError:
                return

            for prop in props:
                editProp(prop)

    def _getContainer(self):
        return Property.properties


class Event(NamedExpression):
    events = dict()

    def __init__(self, name, args, kwargs):
        super(Event, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return Event.events

    @staticmethod
    def add(name, args, kwargs):
        event = Event(name, args, kwargs)
        event.addToContainer()


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