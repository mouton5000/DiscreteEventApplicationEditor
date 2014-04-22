from random import random
from itertools import chain
from dictSet import DictContainer


class BExpression(object):
    def __init__(self, expr):
        self._expr = expr
        self._timer = []
        self._locks = []
        self.listTimersAndLocks()

    def listTimersAndLocks(self):
        check = [self._expr]
        while len(check) != 0:
            e = check.pop()
            if isinstance(e, Timer):
                self._timer.append(e)
            elif isinstance(e, eLock):
                self._locks.append(e)
            try:
                check.append(e.a1)
                check.append(e.a2)
            except AttributeError:
                pass

    def __str__(self):
        return str(self._expr)

    def eval(self):
        return self._expr.eval(dict())

    def init(self):
        for timer in self._timer:
            timer.init()


class BLitteral(object):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def eval(self, previousEvaluation):
        if self._value:
            yield previousEvaluation


class BBiOp(object):
    def __init__(self, a1, a2):
        self._a1 = a1
        self._a2 = a2

    def __str__(self):
        return '(' + str(self._a1) + ' ' + self.symbol + ' ' + str(self._a2) + ')'


class And(BBiOp):
    def __init__(self, a1, a2):
        super(And, self).__init__(a1, a2)
        self.symbol = 'and'

    def eval(self, previousEvaluation):
        return chain(*(self._a2.eval(eval1) for eval1 in self._a1.eval(previousEvaluation) if not eval1 is None))


class Or(BBiOp):
    def __init__(self, a1, a2):
        super(Or, self).__init__(a1, a2)
        self.symbol = 'or'

    def eval(self, previousEvaluation):
        dc = DictContainer()
        for eval1 in self._a1.eval(previousEvaluation):
            dc.add(eval1)
            yield eval1
        for eval2 in self._a2.eval(previousEvaluation):
            if dc.add(eval2):
                yield eval2


class Not(object):
    def __init__(self, a1):
        self._a1 = a1

    def __str__(self):
        return '( not ' + str(self._a1) + ')'

    def eval(self, previousEvaluation):
        try:
            self._a1.eval(previousEvaluation).next()
        except StopIteration:
            yield previousEvaluation


class Timer(object):
    def __init__(self, nbFrames):
        self._nbFrames = nbFrames
        self._nbFramesBeforeTrue = None

    def __str__(self):
        return '( timer ' + str(self._nbFrames) + ')'

    def init(self):
        self._nbFramesBeforeTrue = self._nbFrames

    def eval(self, previousEvaluation):
        self._nbFramesBeforeTrue -= 1
        if self._nbFramesBeforeTrue < 0:
            yield previousEvaluation


class Rand(object):
    def __init__(self, prob):
        self._prob = prob

    def __str__(self):
        return '( rand ' + str(self._prob) + ')'

    def eval(self, previousEvaluation):
        try:
            if self._prob[0].isupper():
                p = previousEvaluation[self._prob]
        except TypeError:
            p = self._prob
        except KeyError:
            yield
        print p
        if random() < p:
            yield previousEvaluation


class eLock(object):
    def __init__(self, priority, *keys):
        self._priority = priority
        self._keys = keys

    def __str__(self):
        return '( elock' + str(self._keys) + ' : ' + str(self._priority) + ')'


class Is(BBiOp):
    def __init__(self, variable, function):
        super(Is, self).__init__(variable, function)
        self.symbol = 'is'

    def eval(self, previousEvaluation):
        if self._a1 in previousEvaluation:
            yield  # The variable must not have already been unified
        try:
            value = self._a2.value(previousEvaluation)
        except (ArithmeticError, TypeError):
            yield  # The arithmetical function can not be evaluated
        else:
            if not value is None:
                neval = previousEvaluation.copy()
                neval[self._a1] = value
                yield neval


class Compare(BBiOp):
    def __init__(self, a1, a2):
        super(Compare, self).__init__(a1, a2)

    def eval(self, previousEvaluation):
        try:
            v1 = self._a1.value(previousEvaluation)
            v2 = self._a2.value(previousEvaluation)
        except (ArithmeticError, TypeError):
            yield  # One of the arithmetical function can not be evaluated
        else:
            if not v1 is None and not v2 is None and self.comp(v1, v2):
                yield previousEvaluation


class Equals(Compare):
    def __init__(self, a1, a2):
        super(Equals, self).__init__(a1, a2)
        self.symbol = '=='

    def comp(self, v1, v2):
        return v1 == v2


class GreaterThan(Compare):
    def __init__(self, a1, a2):
        super(GreaterThan, self).__init__(a1, a2)
        self.symbol = '>'

    def comp(self, v1, v2):
        return v1 > v2


class LowerThan(Compare):
    def __init__(self, a1, a2):
        super(LowerThan, self).__init__(a1, a2)
        self.symbol = '<'

    def comp(self, v1, v2):
        return v1 < v2


class GeqThan(Compare):
    def __init__(self, a1, a2):
        super(GeqThan, self).__init__(a1, a2)
        self.symbol = '>='

    def comp(self, v1, v2):
        return v1 >= v2


class LeqThan(Compare):
    def __init__(self, a1, a2):
        super(LeqThan, self).__init__(a1, a2)
        self.symbol = '<='

    def comp(self, v1, v2):
        return v1 <= v2


class NotEquals(Compare):
    def __init__(self, a1, a2):
        super(NotEquals, self).__init__(a1, a2)
        self.symbol = '!='

    def comp(self, v1, v2):
        return v1 != v2


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

    def weakCompare(self, namedExpr):
        try:
            return self.name == namedExpr.name and len(self) == len(namedExpr)
        except AttributeError:
            return False

    def unify(self, namedExpr, evaluation):
        neval = evaluation.copy()
        for p1, p2 in zip(self, namedExpr):
            try:
                v1 = neval[p1]
            except KeyError:
                v1 = None

            if p1 == '_' or p1 == p2 or v1 == p2:
                continue

            try:
                if not p1[0].isupper() or not v1 is None:  # p1 is not a variable or p1 is identified
                    return
                neval[p1] = p2  # p1 is identified with p2
            except TypeError:
                return
        return neval

    def eval(self, previousEvaluation):
        dc = DictContainer()
        for elem in self.container:
            if not self.weakCompare(elem):
                continue
            neval = self.unify(elem, previousEvaluation)
            if not neval is None and dc.add(neval):
                yield neval

    def eval_update(self, evaluation):
        def evalArg(arg):
            try:
                return evaluation[arg]
            except KeyError:
                return arg

        newArgs = (evalArg(arg) for arg in self)
        return Property(self.name, *newArgs)

    def __hash__(self):
        return hash(self._name) + hash(self._args)

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


if __name__ == '__main__':
    pass