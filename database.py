__author__ = 'mouton'


class NamedExpression(object):

    def __init__(self, name, *args):
        self._name = name
        self._args = args

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

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, obj):
        try:
            return self.name == obj.name and self._args == obj._args
        except AttributeError:
            return False


class Property(NamedExpression):
    properties = set([])

    def __init__(self, name, *args):
        super(Property, self).__init__(name, *args)

    @property
    def container(self):
        return Property.properties


class Event(NamedExpression):
    events = set([])

    def __init__(self, name, *args):
        super(Event, self).__init__(name, *args)


    @property
    def container(self):
        return Event.events


class Variable(object):
    def __init__(self, name):
        if name != '_':
            self._name = name
        else:
            self._name = None

    @property
    def name(self):
        return self._name

    def isUnnamed(self):
        return self._name is None

    def __eq__(self, other):
        try:
            return self.name == other.name or (self.isUnnamed() and other.isUnnamed())
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)