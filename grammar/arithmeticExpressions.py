from database import Variable
from collections import deque


class ALitteral(object):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

    def value(self, evaluation, selfParam=None):
        try:
            return evaluation[self._value]
        except KeyError:
            pass

        if isinstance(self._value, Variable):
            raise ValueError
        else:
            return self._value


class UndefinnedLitteral(object):
    def __init__(self):
        pass

    def __str__(self):
        return '_'

    def __repr__(self):
        return '_'

    def value(self, _, selfParam=None):
        from database import UNDEFINED_PARAMETER
        return UNDEFINED_PARAMETER


class ListLitteral(object):
    def __init__(self, args):
        self._args = args

    def __str__(self):
        return '(' + ','.join([str(o) for o in self._args]) + ')'

    def __repr__(self):
        return '(' + ','.join([str(o) for o in self._args]) + ')'

    def _evalArgs(self, evaluation, selfParam):
        return [arg.value(evaluation, selfParam) for arg in self._args]

    def value(self, evaluation, selfParam=None):
        argsValue = self._evalArgs(evaluation, selfParam)
        return argsValue


class LinkedListLitteral(ListLitteral):
    def __init__(self, args):
        super(LinkedListLitteral, self).__init__(args)

    def value(self, evaluation, selfParam=None):
        argsValue = self._evalArgs(evaluation, selfParam)
        return deque(argsValue)


class SetLitteral(ListLitteral):
    def __init__(self, args):
        super(SetLitteral, self).__init__(args)

    def value(self, evaluation, selfParam=None):
        argsValue = self._evalArgs(evaluation, selfParam)
        return set(argsValue)


class ABiOp(object):
    def __init__(self, a1, a2):
        self._a1 = a1
        self._a2 = a2

    def __str__(self):
        return '(' + str(self._a1) + ' ' + self.symbol + ' ' + str(self._a2) + ')'

    def __repr__(self):
        return '(' + str(self._a1) + ' ' + self.symbol + ' ' + str(self._a2) + ')'

    def value(self, evaluation, selfParam=None):
        v1 = self._a1.value(evaluation, selfParam)
        v2 = self._a2.value(evaluation, selfParam)
        return self.operation(v1, v2)


class Addition(ABiOp):
    def __init__(self, a1, a2):
        super(Addition, self).__init__(a1, a2)
        self.symbol = '+'

    def operation(self, v1, v2):
        try:
            return v1 + v2
        except TypeError:
            return str(v1) + str(v2)


class Subtraction(ABiOp):
    def __init__(self, a1, a2):
        super(Subtraction, self).__init__(a1, a2)
        self.symbol = '-'

    def operation(self, v1, v2):
        return v1 - v2


class Product(ABiOp):
    def __init__(self, a1, a2):
        super(Product, self).__init__(a1, a2)
        self.symbol = '*'

    def operation(self, v1, v2):
        return v1 * v2


class Division(ABiOp):
    def __init__(self, a1, a2):
        super(Division, self).__init__(a1, a2)
        self.symbol = '/'

    def operation(self, v1, v2):
        return float(v1) / float(v2)


class EuclideanDivision(ABiOp):
    def __init__(self, a1, a2):
        super(EuclideanDivision, self).__init__(a1, a2)
        self.symbol = '//'

    def operation(self, v1, v2):
        return v1 // v2


class Modulo(ABiOp):
    def __init__(self, a1, a2):
        super(Modulo, self).__init__(a1, a2)
        self.symbol = '%'

    def operation(self, v1, v2):
        return v1 % v2


class Power(ABiOp):
    def __init__(self, a1, a2):
        super(Power, self).__init__(a1, a2)
        self.symbol = '**'

    def operation(self, v1, v2):
        return v1 ** v2


class GetItemExpression(object):
    def __init__(self, l, index):
        self._list = l
        self._index = index

    def __str__(self):
        return str(self._list) + '[' + str(self._index) + ']'

    def __repr__(self):
        return str(self._list) + '[' + str(self._index) + ']'

    def value(self, evaluation, selfParam=None):
        l1 = self._list.value(evaluation, selfParam)
        if isinstance(l1, (list, deque)):
            a2 = self._index.value(evaluation, selfParam)
            return l1[a2]
        else:
            return next(iter(l1))


class GetSublistExpression(object):
    def __init__(self, l, index1, index2):
        self._list = l
        self._index1 = index1
        self._index2 = index2

    def __str__(self):
        if self._index1 is None:
            if self._index2 is None:
                return str(self._list) + '[:]'
            else:
                return str(self._list) + '[:' + str(self._index2) + ']'
        else:
            if self._index2 is None:
                return str(self._list) + '[' + str(self._index1) + ':]'
            else:
                return str(self._list) + '[' + str(self._index1) + ':' + str(self._index2) + ']'

    def __repr__(self):
        if self._index1 is None:
            if self._index2 is None:
                return str(self._list) + '[:]'
            else:
                return str(self._list) + '[:' + str(self._index2) + ']'
        else:
            if self._index2 is None:
                return str(self._list) + '[' + str(self._index1) + ':]'
            else:
                return str(self._list) + '[' + str(self._index1) + ':' + str(self._index2) + ']'

    def value(self, evaluation, selfParam=None):
        import itertools
        l1 = self._list.value(evaluation, selfParam)
        if self._index1 is None:
            if self._index2 is None:
                return l1
            else:
                a2 = self._index2.value(evaluation, selfParam) % len(l1)
                if isinstance(l1, list):
                    return l1[:a2]
                elif isinstance(l1, deque):
                    return deque(itertools.islice(l1, a2))
                else:
                    it = iter(l1)
                    return set([next(it) for _ in xrange(a2)])
        else:
            a1 = self._index1.value(evaluation, selfParam) % len(l1)
            if self._index2 is None:
                if isinstance(l1, list):
                    return l1[a1:]
                elif isinstance(l1, deque):
                    return deque(itertools.islice(l1, a1, len(l1)))
                else:
                    it = iter(l1)
                    return set([next(it) for _ in xrange(len(l1) - a1)])
            else:
                a2 = self._index2.value(evaluation, selfParam) % len(l1)
                if isinstance(l1, list):
                    return l1[a1:a2]
                elif isinstance(l1, deque):
                    return deque(itertools.islice(l1, a1, a2))
                else:
                    it = iter(l1)
                    return set([next(it) for _ in xrange(a2 - a1)])


class InsertExpression(object):
    def __init__(self, l, index, value):
        self._list = l
        self._index = index
        self._value = value

    def __str__(self):
        if self._index is None:
            return str(self._list) + '<<' + str(self._value)
        else:
            return str(self._list) + '<' + str(self._index) + '<' + str(self._value)

    def __repr__(self):
        if self._index is None:
            return str(self._list) + '<<' + str(self._value)
        else:
            return str(self._list) + '<' + str(self._index) + '<' + str(self._value)

    def value(self, evaluation, selfParam=None):
        l1 = self._list.value(evaluation, selfParam)
        if isinstance(l1, list):
            l2 = l1[:]
        elif isinstance(l1, deque):
            l2 = deque(l1)
        else:
            l2 = l1.copy()

        v = self._value.value(evaluation, selfParam)
        if isinstance(l1, (list, deque)):
            if self._index is None:
                l2.append(v)
            else:
                index = self._index.value(evaluation, selfParam)
                l2.insert(index, v)
        else:
            l2.add(v)
        return l2


class RemoveExpression(object):
    def __init__(self, l, index, value):
        self._list = l
        self._index = index
        self._value = value

    def __str__(self):
        if self._index is None:
            return str(self._list) + '>>' + str(self._value)
        else:
            return str(self._list) + '>' + str(self._index) + '>' + str(self._value)

    def __repr__(self):
        if self._index is None:
            return str(self._list) + '>>' + str(self._value)
        else:
            return str(self._list) + '>' + str(self._index) + '>' + str(self._value)

    def value(self, evaluation, selfParam=None):
        l1 = self._list.value(evaluation, selfParam)
        if isinstance(l1, list):
            l2 = l1[:]
        elif isinstance(l1, deque):
            l2 = deque(l1)
        else:
            l2 = l1.copy()

        if self._index is None:
            v = self._value.value(evaluation, selfParam)
            l2.remove(v)
        else:
            if isinstance(l1, (list, deque)):
                index = self._index.value(evaluation, selfParam)
                l2.pop(index)
            else:
                l2.pop()
        return l2


class RemoveAllExpression(object):
    def __init__(self, l, value):
        self._list = l
        self._value = value

    def __str__(self):
        return str(self._list) + '>>>' + str(self._value)

    def __repr__(self):
        return str(self._list) + '>>>' + str(self._value)

    def value(self, evaluation, selfParam=None):
        l1 = self._list.value(evaluation, selfParam)
        v = self._value.value(evaluation, selfParam)
        if isinstance(l1, set):
            l2 = l1.copy()
            l2.remove(v)
            return l2
        else:
            l2 = [x for x in l1 if x != v]
            if isinstance(l1, list):
                return l2
            else:
                return deque(l2)


class AUnOp(object):
    def __init__(self, a):
        self._a = a

    def __str__(self):
        return self._symbol + '(' + str(self._a) + ')'

    def __repr__(self):
        return self._symbol + '(' + str(self._a) + ')'

    def value(self, evaluation, selfParam=None):
        v = self._a.value(evaluation, selfParam)
        return self.operation(v)


class Func(AUnOp):
    def __init__(self, a, func):
        super(Func, self).__init__(a)
        self._func = func
        self._symbol = str(func)[19:-1]

    def operation(self, v):
        return self._func(v)


class Min(ABiOp):
    def __init__(self, a1, a2):
        super(Min, self).__init__(a1, a2)

    def value(self, evaluation, selfParam=None):
        v1 = self._a1.value(evaluation, selfParam)
        v2 = self._a2.value(evaluation, selfParam)
        return min(v1, v2)


class Max(ABiOp):
    def __init__(self, a1, a2):
        super(Max, self).__init__(a1, a2)

    def value(self, evaluation, selfParam=None):
        v1 = self._a1.value(evaluation, selfParam)
        v2 = self._a2.value(evaluation, selfParam)
        return max(v1, v2)


class SelfExpression():
    def __init__(self):
        pass

    def value(self, _, selfParam=None):
        return selfParam