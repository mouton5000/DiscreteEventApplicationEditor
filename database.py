__author__ = 'mouton'


class UndefinedParameter:
    def __init__(self):
        pass

UNDEFINED_PARAMETER = UndefinedParameter()


class NamedExpression(object):

    def __init__(self, name, args):
        self._name = name
        self._args = list(args)

    def __str__(self):
        return str(self._name) + '(' + ','.join([str(o) for o in self._args]) + ')'

    def __repr__(self):
        return str(self._name) + '(' + ','.join([str(o) for o in self._args]) + ')'

    def __len__(self):
        return len(self._args)

    @property
    def name(self):
        return self._name

    def __iter__(self):
        return iter(self._args)

    def __getitem__(self, index):
        return self._args[index]

    def __setitem__(self, index, value):
        self._args[index] = value

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, obj):
        try:
            return self.name == obj.name and self._args == obj._args
        except AttributeError:
            return False


class Property(NamedExpression):
    properties = set([])

    def __init__(self, name, args):
        super(Property, self).__init__(name, args)

    def filter(self, name, args):
        if name != self.name or len(args) != len(self):
            return False

        def filterArgs(arg, propArg):
            return arg == propArg or arg == UNDEFINED_PARAMETER

        return all(filterArgs(arg, propArg) for arg, propArg in zip(args, self))

    @staticmethod
    def removeAll(name, args):
        Property.properties = {prop for prop in Property.properties if not prop.filter(name, args)}

    @staticmethod
    def edit(name, args1, unevaluatedArgs2, evaluation):
        size = len(args1)
        if size != len(unevaluatedArgs2):
            return
        for prop in Property.properties:
            if not prop.filter(name, args1):
                continue
            for (index, arg), param in zip(enumerate(unevaluatedArgs2), prop):
                newArg = arg.value(evaluation, selfParam=param)
                if newArg == UNDEFINED_PARAMETER:
                    continue
                prop[index] = newArg


    @property
    def container(self):
        return Property.properties


class Event(NamedExpression):
    events = set([])

    def __init__(self, name, args):
        super(Event, self).__init__(name, args)

    @property
    def container(self):
        return Event.events


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