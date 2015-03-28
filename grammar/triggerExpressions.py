import abc
from random import random, randint
from itertools import chain

from utils.dictSet import DictContainer
from database import Variable, Property, Event, UNDEFINED_PARAMETER


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
        if isinstance(key, Variable):
            return self.variables[key]
        else:
            return self.locks[key]

    def __setitem__(self, key, value):
        if isinstance(key, Variable):
            self.variables[key] = value
        else:
            self.locks[key] = value

    def __str__(self):
        return str(self.variables) + ' ' + str(self.locks)

    def __repr__(self):
        return str(self)

    def copy(self):
        e = Evaluation()
        e.variables = self.variables.copy()
        e.locks = self.locks.copy()
        return e

    def __contains__(self, key):
        if isinstance(key, Variable):
            return key in self.variables
        else:
            return key in self.locks

    def __delitem__(self, key):
        if isinstance(key, Variable):
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

    def __eq__(self, other):
        return self.variables == other.variables and self.locks == other.locks


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
                                   if eval1 is not None)


class Or(BBiOp):
    def __init__(self, a1, a2):
        super(Or, self).__init__(a1, a2)
        self.symbol = 'or'

    def eval(self, token, previousEvaluation):
        dc = DictContainer()
        for eval1 in self._a1.eval(token, previousEvaluation):
            dc.add(eval1.variables)
            yield eval1
        for eval2 in self._a2.eval(token, previousEvaluation):
            if dc.add(eval2.variables):
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
        try:
            nbFrames = self._nbFrames.value(previousEvaluation)

            if nbFrames and nbFrames <= token.nbFrameSinceLastMove:
                yield previousEvaluation
        except (ArithmeticError, TypeError, ValueError):
            pass


class Rand(object):
    def __init__(self, prob):
        self._prob = prob

    def __str__(self):
        return '( rand ' + str(self._prob) + ')'

    def eval(self, _, previousEvaluation):
        try:
            prob = self._prob.value(previousEvaluation)
            if random() < prob:
                yield previousEvaluation
        except (ArithmeticError, TypeError, ValueError):
            pass


class RandInt(object):
    def __init__(self, var, maxInt):
        self._var = var
        self._maxInt = maxInt

    def __str__(self):
        return '( randInt ' + str(self._var) + ', ' + str(self._maxInt) + ')'

    def eval(self, _, previousEvaluation):
        try:
            maxInt = int(self._maxInt.value(previousEvaluation))
        except (ArithmeticError, TypeError, ValueError):
            maxInt = -1

        if maxInt > 0:
            j = randint(0, maxInt - 1)

            if isinstance(self._var, Variable):
                try:
                    i = previousEvaluation[self._var]
                    if i == j:
                        yield previousEvaluation
                except KeyError:
                    neval = previousEvaluation.copy()
                    neval[self._var] = j
                    yield neval
            else:
                try:
                    i = self._var.value(previousEvaluation)
                    if int(i) == j:
                        yield previousEvaluation
                except (ArithmeticError, TypeError, ValueError):
                    pass


class eLock(object):
    def __init__(self, priority, keys):
        self._priority = priority
        self._keys = keys

    def __str__(self):
        return '( elock' + str(self._keys) + ' : ' + str(self._priority) + ')'

    def eval(self, _, previousEvaluation):
        try:
            priority = self._priority.value(previousEvaluation)

            evaluation = previousEvaluation.copy()
            keys = self.eval_keys(previousEvaluation)
            if keys not in evaluation or evaluation[keys] <= priority:
                evaluation[keys] = priority
            yield evaluation
        except (ArithmeticError, TypeError, ValueError):
            pass

    def eval_keys(self, evaluation):
        def evalArg(arg):
            return arg.value(evaluation)

        keys = tuple([evalArg(key) for key in self._keys])
        return keys


class Is(BBiOp):
    def __init__(self, variable, function):
        super(Is, self).__init__(variable, function)
        self.symbol = 'is'

    def eval(self, _, previousEvaluation):
        try:
            value = self._a2.value(previousEvaluation)
            if value is not None:
                neval = previousEvaluation.copy()
                neval[self._a1] = value
                yield neval
        except (ArithmeticError, TypeError, ValueError):
            pass


class Compare(BBiOp):
    def __init__(self, a1, a2):
        super(Compare, self).__init__(a1, a2)

    def eval(self, _, previousEvaluation):
        try:
            v1 = self._a1.value(previousEvaluation)
            v2 = self._a2.value(previousEvaluation)

            if v1 == UNDEFINED_PARAMETER or v2 == UNDEFINED_PARAMETER:
                raise TypeError

            if v1 is not None and v2 is not None and self.comp(v1, v2):
                yield previousEvaluation
        except (ArithmeticError, TypeError, ValueError):
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


class ParameterizedExpression(object):
    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        s = '(' + ', '.join([str(o) for o in self._args])
        if len(self._kwargs) != 0:
            s += ', ' + ', '.join([str(k) + ' = ' + str(v) for k, v in self._kwargs.iteritems()])
        s += ')'
        return s

    def __repr__(self):
        s = '(' + ', '.join([str(o) for o in self._args])
        if len(self._kwargs) != 0:
            s += ', ' + ', '.join([str(k) + ' = ' + str(v) for k, v in self._kwargs.iteritems()]) + ')'
        return s

    def lenArgs(self):
        return len(self._args)

    def lenKWArgs(self):
        return len(self._kwargs)

    def iterArgs(self):
        return iter(self._args)

    def getArg(self, index):
        return self._args[index]

    def getKWArg(self, key):
        return self._kwargs[key]

    def unify(self, namedExpr, evaluation):

        def unifyVariable(paramVariable, param, newEvaluation):
            if isinstance(paramVariable, Variable):
                try:
                    v1 = newEvaluation[paramVariable]
                    if v1 == param:
                        return True
                    else:
                        return False
                except KeyError:  # p1 is an unidentified variable
                    newEvaluation[paramVariable] = param  # p1 is identified with p2
                    return True
            else:
                try:
                    v1 = paramVariable.value(newEvaluation)
                    if v1 == UNDEFINED_PARAMETER or v1 == param:
                        return True
                    else:
                        return False
                except (ArithmeticError, TypeError, ValueError):
                    return False

        neval = evaluation.copy()
        for p1, p2 in zip(self.iterArgs(), namedExpr.iterArgs()):
            # p1 is supposed to be an identified or unnamed variable
            if not unifyVariable(p1, p2, neval):
                return

        for k1, p1 in self._kwargs.iteritems():
            try:
                k2 = k1.value(neval)
                p2 = namedExpr.getKWArg(k2)
                if not unifyVariable(p1, p2, neval):
                    return
            except (KeyError, ArithmeticError, TypeError, ValueError):
                return

        return neval


class NamedExpression(ParameterizedExpression):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, args, kwargs):
        super(NamedExpression, self).__init__(args, kwargs)
        self._name = name

    def __str__(self):
        return str(self._name) + super(NamedExpression, self).__str__()

    def __repr__(self):
        return str(self._name) + super(NamedExpression, self).__repr__()

    @property
    def name(self):
        return self._name

    def weakCompare(self, namedExpr):
        try:
            return \
                self.name == namedExpr.name and \
                self.lenArgs() == namedExpr.lenArgs() and \
                self.lenKWArgs() <= namedExpr.lenKWArgs()
        except AttributeError:
            return False

    @property
    def container(self):
        return self._getContainer()

    @abc.abstractmethod
    def _getContainer(self):
        return

    def eval(self, _, previousEvaluation):
        dc = DictContainer()
        try:
            expressions = self.container[self.name]
        except KeyError:
            return
        for namedExpr in expressions:
            if not self.weakCompare(namedExpr):
                continue
            neval = self.unify(namedExpr, previousEvaluation)
            if neval is not None and dc.add(neval.variables):
                yield neval

    def __hash__(self):
        return hash(self._name) + hash(self._args)

    def __eq__(self, obj):
        try:
            return self.name == obj.name and self._args == obj._args
        except AttributeError:
            return False


class PropertyTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(PropertyTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return Property.properties


class EventTriggerExpression(NamedExpression):
    events = set([])

    def __init__(self, name, args, kwargs):
        super(EventTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return Event.events


class TokenExpression(ParameterizedExpression):
    def __init__(self, args, kwargs):
        super(TokenExpression, self).__init__(args, kwargs)

    def __str__(self):
        return 'TokenExpression' + super(TokenExpression, self).__str__()

    def __repr__(self):
        return 'TokenExpression' + super(TokenExpression, self).__repr__()

    def weakCompare(self, token):
        try:
            return self.lenArgs() == token.lenArgs() and self.lenKWArgs() <= token.lenKWArgs()
        except AttributeError:
            return False

    def eval(self, token, previousEvaluation):
        if self.weakCompare(token):
            neval = self.unify(token, previousEvaluation)
            if neval is not None:
                yield neval


class Any(object):
    def __init__(self, expr):
        super(Any, self).__init__()
        self._expr = expr

    def __str__(self):
        return 'Any(' + str(self._expr) + ')'

    def __repr__(self):
        return 'Any(' + str(self._expr) + ')'

    def eval(self, token, previousEvaluation):
        evaluations = self._expr.eval(token, previousEvaluation)
        try:
            yield evaluations.next()
        except StopIteration:
            pass


class Random(object):
    def __init__(self, expr):
        super(Random, self).__init__()
        self._expr = expr

    def __str__(self):
        return 'Random(' + str(self._expr) + ')'

    def __repr__(self):
        return 'Random(' + str(self._expr) + ')'

    def eval(self, token, previousEvaluation):
        evaluations = self._expr.eval(token, previousEvaluation)

        selected_evaluation = None

        for index, evaluation in enumerate(evaluations):
            if randint(0, index) == 0:
                selected_evaluation = evaluation

        if selected_evaluation is not None:
            yield selected_evaluation


if __name__ == '__main__':
    pass