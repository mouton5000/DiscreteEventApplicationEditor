from database import Variable
from collections import deque
from database import UNDEFINED_PARAMETER
import game.gameWindow as gameWindow


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

    def export(self):
        try:
            exportValue = self._value.export()
        except AttributeError:
            if isinstance(self._value, basestring):
                exportValue = '\'' + self._value + '\''
            else:
                exportValue = str(self._value)
        return 'ALitteral(' + exportValue + ')'


class UndefinedLitteral(object):
    def __init__(self):
        pass

    def __str__(self):
        return '_'

    def __repr__(self):
        return '_'

    def value(self, _, selfParam=None):
        from database import UNDEFINED_PARAMETER
        return UNDEFINED_PARAMETER

    def export(self):
        return 'UndefinedLitteral()'


# class ListLitteral(object):
#     def __init__(self, args):
#         self._args = args
#
#     def __str__(self):
#         return '(' + ','.join([str(o) for o in self._args]) + ')'
#
#     def __repr__(self):
#         return '(' + ','.join([str(o) for o in self._args]) + ')'
#
#     def _evalArgs(self, evaluation, selfParam):
#         return [arg.value(evaluation, selfParam) for arg in self._args]
#
#     def value(self, evaluation, selfParam=None):
#         argsValue = self._evalArgs(evaluation, selfParam)
#         return argsValue
#

# class LinkedListLitteral(ListLitteral):
#     def __init__(self, args):
#         super(LinkedListLitteral, self).__init__(args)
#
#     def value(self, evaluation, selfParam=None):
#         argsValue = self._evalArgs(evaluation, selfParam)
#         return deque(argsValue)
#
#
# class SetLitteral(ListLitteral):
#     def __init__(self, args):
#         super(SetLitteral, self).__init__(args)
#
#     def value(self, evaluation, selfParam=None):
#         argsValue = self._evalArgs(evaluation, selfParam)
#         return set(argsValue)


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

        if v1 == UNDEFINED_PARAMETER or v2 == UNDEFINED_PARAMETER:
            raise TypeError
        return self.operation(v1, v2)

    def export(self):
        return self.__class__.__name__ + '(' + self._a1.export() + ', ' + self._a2.export() + ')'

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


class Min(ABiOp):
    def __init__(self, a1, a2):
        super(Min, self).__init__(a1, a2)
        self.symbol = 'min'

    def operation(self, v1, v2):
        return min(v1, v2)


class Max(ABiOp):
    def __init__(self, a1, a2):
        super(Max, self).__init__(a1, a2)
        self.symbol = 'max'

    def operation(self, v1, v2):
        return max(v1, v2)


# class GetItemExpression(object):
#     def __init__(self, l, index):
#         self._list = l
#         self._index = index
#
#     def __str__(self):
#         return str(self._list) + '[' + str(self._index) + ']'
#
#     def __repr__(self):
#         return str(self._list) + '[' + str(self._index) + ']'
#
#     def value(self, evaluation, selfParam=None):
#         l1 = self._list.value(evaluation, selfParam)
#         a2 = self._index.value(evaluation, selfParam)
#         if isinstance(l1, (list, deque)):
#             return l1[a2]
#         else:
#             if a2 != UNDEFINED_PARAMETER:
#                 raise TypeError
#             return next(iter(l1))
#
#
# class GetSublistExpression(object):
#     def __init__(self, l, index1, index2):
#         self._list = l
#         self._index1 = index1
#         self._index2 = index2
#
#     def __str__(self):
#         if self._index1 is None:
#             if self._index2 is None:
#                 return str(self._list) + '[:]'
#             else:
#                 return str(self._list) + '[:' + str(self._index2) + ']'
#         else:
#             if self._index2 is None:
#                 return str(self._list) + '[' + str(self._index1) + ':]'
#             else:
#                 return str(self._list) + '[' + str(self._index1) + ':' + str(self._index2) + ']'
#
#     def __repr__(self):
#         if self._index1 is None:
#             if self._index2 is None:
#                 return str(self._list) + '[:]'
#             else:
#                 return str(self._list) + '[:' + str(self._index2) + ']'
#         else:
#             if self._index2 is None:
#                 return str(self._list) + '[' + str(self._index1) + ':]'
#             else:
#                 return str(self._list) + '[' + str(self._index1) + ':' + str(self._index2) + ']'
#
#     def value(self, evaluation, selfParam=None):
#         import itertools
#         l1 = self._list.value(evaluation, selfParam)
#
#         try:
#             a1 = self._index1.value(evaluation, selfParam)
#         except AttributeError:
#             a1 = None
#
#         try:
#             a2 = self._index2.value(evaluation, selfParam)
#         except AttributeError:
#             a2 = None
#
#         if not isinstance(a1, int) and a1 is not None:
#             raise TypeError
#         if not isinstance(a2, int) and a2 is not None:
#             raise TypeError
#
#         if isinstance(l1, list):
#             return l1[a1:a2]
#
#         elif isinstance(l1, deque):
#             def rebound(value, length):
#                 if value is not None:
#                     value = min(value, length)
#                     value = max(value, -length)
#                     if value < 0:
#                         value += length
#                 return value
#             a1 = rebound(a1, len(l1))
#             a2 = rebound(a2, len(l1))
#             return deque(itertools.islice(l1, a1, a2))
#
#         else:
#             if a1 is not None:
#                 raise TypeError
#
#             it = iter(l1)
#             if a2 is None:
#                 sliceLen = len(l1)
#             else:
#                 if a2 > 0:
#                     sliceLen = min(len(l1), a2)
#                 else:
#                     sliceLen = max(0, len(l1) + a2)
#             return set([next(it) for _ in xrange(sliceLen)])
#
#
# class InsertExpression(object):
#     def __init__(self, l, index, value):
#         self._list = l
#         self._index = index
#         self._value = value
#
#     def __str__(self):
#         if self._index is None:
#             return str(self._list) + '<<' + str(self._value)
#         else:
#             return str(self._list) + '<' + str(self._index) + '<' + str(self._value)
#
#     def __repr__(self):
#         if self._index is None:
#             return str(self._list) + '<<' + str(self._value)
#         else:
#             return str(self._list) + '<' + str(self._index) + '<' + str(self._value)
#
#     def value(self, evaluation, selfParam=None):
#         l1 = self._list.value(evaluation, selfParam)
#         if isinstance(l1, list):
#             l2 = l1[:]
#         elif isinstance(l1, deque):
#             l2 = deque(l1)
#         else:
#             l2 = l1.copy()
#
#         v = self._value.value(evaluation, selfParam)
#         if isinstance(l1, (list, deque)):
#             if self._index is None:
#                 l2.append(v)
#             else:
#                 index = self._index.value(evaluation, selfParam)
#                 l2.insert(index, v)
#         else:
#             l2.add(v)
#         return l2
#
#
# class RemoveExpression(object):
#     def __init__(self, l, index, value):
#         self._list = l
#         self._index = index
#         self._value = value
#
#     def __str__(self):
#         if self._index is None:
#             return str(self._list) + '>>' + str(self._value)
#         else:
#             return str(self._list) + '>' + str(self._index) + '>' + str(self._value)
#
#     def __repr__(self):
#         if self._index is None:
#             return str(self._list) + '>>' + str(self._value)
#         else:
#             return str(self._list) + '>' + str(self._index) + '>' + str(self._value)
#
#     def value(self, evaluation, selfParam=None):
#         l1 = self._list.value(evaluation, selfParam)
#         if isinstance(l1, list):
#             l2 = l1[:]
#         elif isinstance(l1, deque):
#             l2 = deque(l1)
#         else:
#             l2 = l1.copy()
#
#         if self._index is None:
#             v = self._value.value(evaluation, selfParam)
#             l2.remove(v)
#         else:
#             if isinstance(l1, (list, deque)):
#                 index = self._index.value(evaluation, selfParam)
#                 l2.pop(index)
#             else:
#                 l2.pop()
#         return l2
#
#
# class RemoveAllExpression(object):
#     def __init__(self, l, value):
#         self._list = l
#         self._value = value
#
#     def __str__(self):
#         return str(self._list) + '>>>' + str(self._value)
#
#     def __repr__(self):
#         return str(self._list) + '>>>' + str(self._value)
#
#     def value(self, evaluation, selfParam=None):
#         l1 = self._list.value(evaluation, selfParam)
#         v = self._value.value(evaluation, selfParam)
#         if isinstance(l1, set):
#             l2 = l1.copy()
#             l2.remove(v)
#             return l2
#         else:
#             l2 = [x for x in l1 if x != v]
#             if isinstance(l1, list):
#                 return l2
#             else:
#                 return deque(l2)


class AUnOp(object):
    def __init__(self, a):
        self._a = a

    def __str__(self):
        return self._symbol + '(' + str(self._a) + ')'

    def __repr__(self):
        return self._symbol + '(' + str(self._a) + ')'

    def value(self, evaluation, selfParam=None):
        v = self._a.value(evaluation, selfParam)

        if v == UNDEFINED_PARAMETER:
            raise TypeError

        return self.operation(v)


class Func(AUnOp):
    def __init__(self, a, func):
        super(Func, self).__init__(a)
        self._func = func
        self._symbol = str(func)[19:-1]

    def operation(self, v):
        return self._func(v)

    def export(self):
        return 'Func(' + self._a.export() + ', ' + str(self._func.__name__) + ')'


class _GlobalFPS(object):
    def __init__(self):
        pass

    def __str__(self):
        return 'globals(fps)'

    def value(self, _, selfParam=None):
        return gameWindow.getFps()

    def export(self):
        return 'globalsFpsExpression'

globalsFpsExpression = _GlobalFPS()


class _GlobalWidth(object):
    def __init__(self):
        pass

    def __str__(self):
        return 'globals(width)'

    def value(self, _, selfParam=None):
        return gameWindow.getWidth()

    def export(self):
        return 'globalsWidthExpression'

globalsWidthExpression = _GlobalWidth()


class _GlobalHeight(object):
    def __init__(self):
        pass

    def __str__(self):
        return 'globals(height)'

    def value(self, _, selfParam=None):
        return gameWindow.getHeight()

    def export(self):
        return 'globalsHeightExpression'

globalsHeightExpression = _GlobalHeight()


class SelfLitteral():
    def __init__(self):
        pass

    def value(self, _, selfParam=None):
        if selfParam is None:
            raise ValueError
        return selfParam

    def export(self):
        return 'SelfLitteral()'