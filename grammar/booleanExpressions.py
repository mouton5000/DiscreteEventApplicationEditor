from random import random, randint
from itertools import chain
from dictSet import DictContainer


class BExpression(object):
    def __init__(self, expr):
        self._expr = expr
        self._timers = []
        self._locks = []
        self.listTimersAndLocks()

    def listTimersAndLocks(self):
        check = [self._expr]
        while len(check) != 0:
            e = check.pop()
            if isinstance(e, Timer):
                self._timers.append(e)
            elif isinstance(e, eLock):
                self._locks.append(e)
            try:
                check.append(e._a1)
                check.append(e._a2)
            except AttributeError:
                pass

    def __str__(self):
        return str(self._expr)

    def eval(self, token):
        return self._expr.eval(token, Evaluation())


class Evaluation(object):
    def __init__(self):
        self.variables = dict()
        self.locks = dict()

    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self.variables[key]
        else:
            return self.locks[key]

    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            self.variables[key] = value
        else:
            self.locks[key] = value

    def __str__(self):
        return str(self.variables) + ' ' + str(self.locks)

    def copy(self):
        e = Evaluation()
        e.variables = self.variables.copy()
        e.locks = self.locks.copy()
        return e

    def __contains__(self, key):
        if isinstance(key, basestring):
            return key in self.variables
        else:
            return key in self.locks

    def __delitem__(self, key):
        if isinstance(key, basestring):
            del self.variables[key]
        else:
            del self.locks[key]

    def __len__(self):
        return len(self.variables) + len(self.locks)

    def popitem(self):
        try:
            return self.variables.popitem()
        except KeyError:
            return self.locks.popitem()


class BLitteral(object):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def eval(self, _, previousEvaluation):
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

    def eval(self, token, previousEvaluation):
        return chain.from_iterable(self._a2.eval(token, eval1) for eval1 in self._a1.eval(token, previousEvaluation)
                                   if not eval1 is None)


class Or(BBiOp):
    def __init__(self, a1, a2):
        super(Or, self).__init__(a1, a2)
        self.symbol = 'or'

    def eval(self, token, previousEvaluation):
        dc = DictContainer()
        for eval1 in self._a1.eval(token, previousEvaluation):
            dc.add(eval1)
            yield eval1
        for eval2 in self._a2.eval(token, previousEvaluation):
            if dc.add(eval2):
                yield eval2


class Not(object):
    def __init__(self, a1):
        self._a1 = a1

    def __str__(self):
        return '( not ' + str(self._a1) + ')'

    def eval(self, token, previousEvaluation):
        try:
            self._a1.eval(token, previousEvaluation).next()
        except StopIteration:
            yield previousEvaluation


class Timer(object):
    def __init__(self, nbFrames):
        self._nbFrames = nbFrames

    def __str__(self):
        return '( timer ' + str(self._nbFrames) + ')'

    def eval(self, token, previousEvaluation):
        #print token, previousEvaluation, self, self._nbFrames <= token.nbFrameSinceLastMove
        if self._nbFrames <= token.nbFrameSinceLastMove:
            yield previousEvaluation


class Rand(object):
    def __init__(self, prob):
        self._prob = prob

    def __str__(self):
        return '( rand ' + str(self._prob) + ')'

    def eval(self, _, previousEvaluation):
        try:
            if self._prob[0].isupper():
                p = previousEvaluation[self._prob]
                if random() < p:
                    yield previousEvaluation
        except TypeError:
            p = self._prob
            if random() < p:
                yield previousEvaluation
        except KeyError:
            pass


class RandInt(object):
    def __init__(self, var, max):
        self._var = var
        self._max = max

    def __str__(self):
        return '( randInt ' + str(self._var) + ', ' + str(self._max) + ')'

    def eval(self, _, previousEvaluation):
        j = randint(0, self._max - 1)
        try:
            i = previousEvaluation[self._var]
            if i == j:
                yield previousEvaluation
        except KeyError:
            neval = previousEvaluation.copy()
            neval[self._var] = j
            yield neval


class eLock(object):
    def __init__(self, priority, *keys):
        self._priority = priority
        self._keys = keys

    def __str__(self):
        return '( elock' + str(self._keys) + ' : ' + str(self._priority) + ')'

    def eval(self, _, previousEvaluation):
        evaluation = previousEvaluation.copy()
        try:
            keys = self.eval_keys(previousEvaluation)
            if not keys in evaluation or evaluation[keys] <= self._priority:
                evaluation[keys] = self._priority
            yield evaluation
        except KeyError:
            pass

    def eval_keys(self, evaluation):
        def evalArg(arg):
            try:
                if arg[0].isupper():
                    return evaluation[arg]
                else:
                    return arg
            except TypeError:
                return arg

        keys = tuple([evalArg(key) for key in self._keys])
        return keys


class Is(BBiOp):
    def __init__(self, variable, function):
        super(Is, self).__init__(variable, function)
        self.symbol = 'is'

    def eval(self, _, previousEvaluation):
        if not self._a1 in previousEvaluation:
            try:
                value = self._a2.value(previousEvaluation)
                if not value is None:
                    neval = previousEvaluation.copy()
                    neval[self._a1] = value
                    yield neval
            except (ArithmeticError, TypeError, ValueError):
                pass


class Compare(BBiOp):
    def __init__(self, a1, a2):
        super(Compare, self).__init__(a1, a2)

    def eval(self, token, previousEvaluation):
        try:
            v1 = self._a1.value(previousEvaluation)
            v2 = self._a2.value(previousEvaluation)
            #print token, previousEvaluation, v1, v2
            if not v1 is None and not v2 is None and self.comp(v1, v2):
                yield previousEvaluation
        except (ArithmeticError, TypeError):
            pass


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

    def eval(self, _, previousEvaluation):
        dc = DictContainer()
        for elem in self.container:
            if not self.weakCompare(elem):
                continue
            neval = self.unify(elem, previousEvaluation)
            if not neval is None and dc.add(neval):
                yield neval

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

    def eval_update(self, evaluation):
        def evalArg(arg):
            try:
                return evaluation[arg]
            except KeyError:
                return arg

        newArgs = (evalArg(arg) for arg in self)
        return Property(self.name, *newArgs)


class Event(NamedExpression):
    events = set([])

    def __init__(self, name, *args):
        super(Event, self).__init__(name, *args)

    @property
    def container(self):
        return Event.events

    def eval_update(self, evaluation):
        def evalArg(arg):
            try:
                return evaluation[arg]
            except KeyError:
                return arg

        newArgs = (evalArg(arg) for arg in self)
        return Event(self.name, *newArgs)


class TokenExpression:
    def __init__(self, *args):
        self._args = args

    def __str__(self):
        return 'TokenExpression(' + ','.join([str(o) for o in self._args]) + ')'

    def __repr__(self):
        return 'TokenExpression(' + ','.join([str(o) for o in self._args]) + ')'

    def __len__(self):
        return len(self._args)

    def __iter__(self):
        return iter(self._args)

    def __getitem__(self, index):
        return self._args[index]

    def weakCompare(self, token):
        try:
            return len(self) <= len(token)
        except AttributeError:
            return False

    def unify(self, token, evaluation):
        neval = evaluation.copy()
        for p1, p2 in zip(self, token):
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

    def eval(self, token, previousEvaluation):
        if self.weakCompare(token):
            neval = self.unify(token, previousEvaluation)
            if not neval is None:
                yield neval


if __name__ == '__main__':
    pass