class DictContainer:
    """
    A container for dictionnaries such that each dict is unique.
    """
    def __init__(self):
        self._tree = _DictTree(isRoot=True)

    def add(self, d):
        return self._tree.add(d, set([]))


class _DictTree:
    def __init__(self, label=None, value=None, isRoot=False):
        self._label = label
        self._value = value
        self._children = []
        self._isFinal = False
        self._isRoot = isRoot

    def add(self, kwargs, readKWArgs):
        newReadKWArgs = readKWArgs
        if not self._isRoot:  # node is not root
            try:
                if kwargs[self._label] != self._value:
                    return None  # This dict can not be added into that subtree
                newReadKWArgs.add(self._label)
            except KeyError:
                return None  # This dict can not be added into that subtree

        if len(kwargs) == len(newReadKWArgs):
            if self._isFinal:
                return False  # The container already contains the dictionnary
            else:
                self._isFinal = True
                return True  # The dictionnary was successfully added

        for child in self._children:
            added = child.add(kwargs, newReadKWArgs)
            if added is not None:
                return added
        self._appendRemaining(kwargs, newReadKWArgs)
        return True

    def _appendRemaining(self, kwargs, readKWArgs):
        t = self

        for key, value in kwargs.iteritems():
            if key not in readKWArgs:
                ch = _DictTree(label=key, isRoot=False, value=value)
                t._children.append(ch)
                t = ch

        t._isFinal = True


if __name__ == '__main__':
    dc = DictContainer()

    dct = {'Y': 'abc', 'X': 1, 'Z': 12.0, 'T': True}

    print dc.add(dct)
    print dc.add(dct)