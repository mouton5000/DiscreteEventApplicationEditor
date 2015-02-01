class DictContainer:
    """
    A container for dictionnaries such that each dict is unique.
    """
    def __init__(self):
        self._tree = _DictTree()

    def add(self, d):
        return self._tree.addDict(d.copy())


class _Root:
    def __init__(self):
        pass


class _Leaf:
    def __init__(self):
        pass


class _DictTree:
    _ROOT = _Root()

    def __init__(self, label=_ROOT, value=None):
        self._label = label
        self._value = value
        self._children = []
        self._isFinal = False

    def addDict(self, d):
        if self._label != _DictTree._ROOT:
            try:
                if d[self._label] != self._value:
                    return None  # This dict can not be added into that subtree
                del d[self._label]
            except KeyError:
                return None  # This dict can not be added into that subtree

        if len(d) == 0:
            if self._isFinal:
                return False  # The container already contains the dictionnary
            else:
                self._isFinal = True
                return True  # The dictionnary was successfully added

        for child in self._children:
            added = child.addDict(d)
            if added is not None:
                return added
        self._appendRemaining(d)
        return True

    def _appendRemaining(self, d):
        try:
            key, value = d.popitem()
            t = _DictTree(key, value)
            self._children.append(t)
            t._appendRemaining(d)
        except KeyError:
            self._isFinal = True