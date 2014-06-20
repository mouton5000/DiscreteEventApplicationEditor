__author__ = 'mouton'


class Property():
    properties = set([])

    def __init__(self, name, *args):
        super(Property, self).__init__()
        self._name = name
        self._args = args

    @property
    def container(self):
        return Property.properties


class Event():
    events = set([])

    def __init__(self, name, *args):
        super(Event, self).__init__()
        self._name = name
        self._args = args

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