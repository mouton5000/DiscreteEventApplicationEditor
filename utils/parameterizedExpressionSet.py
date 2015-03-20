from database import UNDEFINED_PARAMETER


class ParameterizedExpressionContainer:
    """
    A container for dictionnaries such that each dict is unique.
    """
    def __init__(self):
        self._tree = _ParameterizedExpressionTree()

    def add(self, l, d):
        return self._tree.add(l, 0, d, set([]))

    def contains(self, l, d):
        return self._tree.contains(l, d)

    def remove(self, l, d):
        return self._tree.removeAll(l, d)


class _ParameterizedExpressionTree:
    def __init__(self, label=None, isArg=False, value=None, father=None):
        self._label = label
        self._isArg = isArg
        self._value = value
        self._father = father
        if father is not None:
            self._father._children.append(self)
        self._children = []
        self._isFinal = False

    def add(self, args, nbReadArgs, kwargs, readKWArgs):
        newNbReadArgs = nbReadArgs
        newReadKWArgs = readKWArgs
        if self._father is not None:  # node is not root
            if nbReadArgs < len(args):
                if not self._isArg:
                    return None
                if args[nbReadArgs] != self._label:
                    return None
                newNbReadArgs += 1
            else:
                if self._isArg:
                    return None
                try:
                    if kwargs[self._label] != self._value:
                        return None  # This dict can not be added into that subtree
                    newReadKWArgs.add(self._label)
                except KeyError:
                    return None  # This dict can not be added into that subtree

        if len(args) == newNbReadArgs and len(kwargs) == len(newReadKWArgs):
            if self._isFinal:
                return False  # The container already contains the dictionnary
            else:
                self._isFinal = True
                return True  # The dictionnary was successfully added

        for child in self._children:
            added = child.add(args, newNbReadArgs, kwargs, newReadKWArgs)
            if added is not None:
                return added
        self._appendRemaining(args, newNbReadArgs, kwargs, newReadKWArgs)
        return True

    def _appendRemaining(self, args, nbReadArgs, kwargs, readKWArgs):
        t = self

        for arg in args[nbReadArgs:]:
            t = _ParameterizedExpressionTree(arg, True, None, t)

        for key, value in kwargs.iteritems():
            if key not in readKWArgs:
                t = _ParameterizedExpressionTree(key, False, value, t)

        t._isFinal = True

    def contains(self, args, kwargs):
        return self.nodeContaining(args, 0, kwargs, 0) is not None

    def nodeContaining(self, args, nbReadArgs, kwargs, nbReadKWArgs):
        '''
        @param args:
        @param nbReadArgs:
        @param kwargs:
        @param nbReadKWArgs:
        @return: a final node corresponding to arg and kwargs
        '''

        newNbReadArgs = nbReadArgs
        newNbReadKWArgs = nbReadKWArgs
        if self._father is not None:  # node is not root
            if self._isArg:
                if len(args) <= newNbReadArgs:
                    return None
                arg = args[nbReadArgs]
                if arg != UNDEFINED_PARAMETER and arg != self._label:
                    return None
                newNbReadArgs += 1
            else:
                if len(kwargs) <= newNbReadKWArgs:
                    return self
                try:
                    if kwargs[self._label] != self._value:
                        return None  # This dict can not be added into that subtree
                    newNbReadKWArgs += 1
                except KeyError:
                    pass

        if len(args) <= newNbReadArgs and len(kwargs) <= newNbReadKWArgs:
            return self

        for child in self._children:
            node = child.nodeContaining(args, newNbReadArgs, kwargs, newNbReadKWArgs)
            if node is not None:
                return node
        return None

    def removeAll(self, args, kwargs):


        nodes = self.nodesContaining(args, 0, kwargs, 0)
        for node in nodes:
            node._isFinal = False

        toPrune = [node for node in nodes if len(node._children) == 0]
        print toPrune


        visited = set([])
        while len(toPrune) > 0:
            node = toPrune.pop()
            if node in visited:
                continue

            father = node._father
            if father is not None and len(node._children) == 0 and not node._isFinal:
                father._children.remove(node)
                toPrune.append(father)
                visited.add(node)



    def nodesContaining(self, args, nbReadArgs, kwargs, nbReadKWArgs):
        '''
        @param args:
        @param nbReadArgs:
        @param kwargs:
        @param nbReadKWArgs:
        @return: a final node corresponding to arg and kwargs
        '''

        newNbReadArgs = nbReadArgs
        newNbReadKWArgs = nbReadKWArgs
        if self._father is not None:  # node is not root
            if newNbReadArgs < len(args):
                if not self._isArg:
                    return []
                arg = args[nbReadArgs]
                if arg != UNDEFINED_PARAMETER and arg != self._label:
                    return []
                newNbReadArgs += 1
            else:
                if self._isArg:
                    return []
                try:
                    if kwargs[self._label] != self._value:
                        return []  # This dict can not be added into that subtree
                    newNbReadKWArgs += 1
                except KeyError:
                    pass

        nodes = []
        if len(args) <= newNbReadArgs and len(kwargs) <= newNbReadKWArgs:
            if self._isFinal:
                nodes = [self]  # The container already contains the dictionnary

        import operator
        return reduce(operator.add, (child.nodesContaining(args, newNbReadArgs, kwargs, newNbReadKWArgs)
                                     for child in self._children), nodes)

    def __str__(self):
        l = []
        node = self
        while node is not None:
            l.insert(0, node)
            node = node._father

        s = ''
        for node in l[:-1]:
            s += str(node._label) + ':' + str(node._value)
            s += ' -> '
        node = l[-1]
        s += str(node._label) + ':' + str(node._value)
        return s

    def __repr__(self):
        return str(self)


def printTree(dt, h):
    print h * '   ', dt._label, dt._value, dt._isFinal
    for ch in dt._children:
        printTree(ch, h + 1)

if __name__ == '__main__':
    dt = _ParameterizedExpressionTree()
    print dt.add([1, 2], 0, {}, set([]))
    print dt.add([1, 2], 0, {2: 1, 1: 1}, set([]))
    print dt.add([1, 2], 0, {2: 1, 1: 2}, set([]))
    print dt.add([1, 2], 0, {2: 1, 1: 2}, set([]))
    print dt.add([2, 1], 0, {1: 1}, set([]))
    print dt.add([1, 2], 0, {1: 1, 2: 1}, set([]))
    print dt.add([2, 1], 0, {2: 1}, set([]))
    print dt.add([2, 1], 0, {2: 1, 3: 1}, set([]))
    print dt.add([2, 1], 0, {4: 1, 2: 1, 5: 1, 6: 1, 7: 1}, set([]))

    print dt.add([2, 1, 4], 0, {4: 1, 2: 1}, set([]))
    print dt.add([2, 1, 5], 0, {4: 1, 2: 1}, set([]))
    print dt.add([2, 1, 4], 0, {4: 1, 2: 1}, set([]))
    print dt.add([2], 0, {4: 1, 2: 1}, set([]))
    print dt.add([2, 1, 4, 5], 0, {4: 1, 2: 1}, set([]))

    printTree(dt, 0)

    print
    print dt.contains([1, 2], {})
    print dt.contains([1, 2], {2: 1, 1: 1})
    print dt.contains([1, 2], {1: 1, 2: 1})
    print dt.contains([1, 2], {3: 1, 2: 1})
    print dt.contains([1, 2], {2: 1, 3: 1})
    print dt.contains([], {})
    print dt.contains([2, 1], {})
    print dt.contains([1, UNDEFINED_PARAMETER], {})
    print dt.contains([UNDEFINED_PARAMETER, UNDEFINED_PARAMETER], {})
    print dt.contains([UNDEFINED_PARAMETER], {})

    print
    print dt.nodesContaining([1, 2], 0, {}, 0)
    print dt.nodesContaining([2, 1], 0, {}, 0)
    print dt.nodesContaining([1, 2], 0, {1: 1}, 0)
    print dt.nodesContaining([1, 2], 0, {1: 2}, 0)
    print dt.nodesContaining([1, 2], 0, {2: 1}, 0)
    #
    # print dt.nodesContaining([UNDEFINED_PARAMETER], 0, {}, 0)
    print dt.nodesContaining([UNDEFINED_PARAMETER, UNDEFINED_PARAMETER], 0, {}, 0)
    #
    # print dt.nodesContaining([UNDEFINED_PARAMETER, UNDEFINED_PARAMETER, UNDEFINED_PARAMETER], 0, {}, 0)
    #
    print
    dt.removeAll([2, 1], {})
    printTree(dt, 0)