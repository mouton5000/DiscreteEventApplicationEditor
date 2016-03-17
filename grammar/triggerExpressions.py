import abc
from random import randint
from itertools import chain

from utils.dictSet import DictContainer
from database import Variable, \
    Property, Event, \
    SpriteProperty, TextProperty, LineProperty, \
    OvalProperty, RectProperty, PolygonProperty, \
    UNDEFINED_PARAMETER, KEYWORD_ID


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
        return self._expr.eval(token, token.evaluation)

    def export(self):
        return 'BExpression(' + self._expr.export() + ')'


class BLitteral(object):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def eval(self, _, previousEvaluation):
        if self._value:
            yield previousEvaluation

    def export(self):
        return 'BLitteral(' + str(self._value) + ')'


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

    def export(self):
        return 'And(' + self._a1.export() + ',' + self._a2.export() + ')'


class Or(BBiOp):
    def __init__(self, a1, a2):
        super(Or, self).__init__(a1, a2)
        self.symbol = 'or'

    def eval(self, token, previousEvaluation):
        for eval1 in self._a1.eval(token, previousEvaluation):
            yield eval1
        for eval2 in self._a2.eval(token, previousEvaluation):
            yield eval2

    def export(self):
        return 'Or(' + self._a1.export() + ',' + self._a2.export() + ')'


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

    def export(self):
        return 'Not(' + self._a1.export() + ')'


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

    def export(self):
        return 'Timer(' + self._nbFrames.export() + ')'


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

    def export(self):
        return 'eLock(' + self._priority.export() + ',' + self._keys.export() + ')'


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

    def export(self):
        return 'Is(' + self._a1.export() + ',' + self._a2.export() + ')'


class Del(object):
    def __init__(self, variable):
        self._a1 = variable

    def eval(self, _, previousEvaluation):
        neval = previousEvaluation.copy()
        try:
            del neval[self._a1]
        except KeyError:
            pass
        yield neval

    def export(self):
        return 'Del(' + self._a1.export() + ')'


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

    def export(self):
        return 'Equals(' + self._a1.export() + ',' + self._a2.export() + ')'


class GreaterThan(Compare):
    def __init__(self, a1, a2):
        super(GreaterThan, self).__init__(a1, a2)
        self.symbol = '>'

    def comp(self, v1, v2):
        return v1 > v2

    def export(self):
        return 'GreaterThan(' + self._a1.export() + ',' + self._a2.export() + ')'


class LowerThan(Compare):
    def __init__(self, a1, a2):
        super(LowerThan, self).__init__(a1, a2)
        self.symbol = '<'

    def comp(self, v1, v2):
        return v1 < v2

    def export(self):
        return 'LowerThan(' + self._a1.export() + ',' + self._a2.export() + ')'


class GeqThan(Compare):
    def __init__(self, a1, a2):
        super(GeqThan, self).__init__(a1, a2)
        self.symbol = '>='

    def comp(self, v1, v2):
        return v1 >= v2

    def export(self):
        return 'GeqThan(' + self._a1.export() + ',' + self._a2.export() + ')'


class LeqThan(Compare):
    def __init__(self, a1, a2):
        super(LeqThan, self).__init__(a1, a2)
        self.symbol = '<='

    def comp(self, v1, v2):
        return v1 <= v2

    def export(self):
        return 'LeqThan(' + self._a1.export() + ',' + self._a2.export() + ')'


class NotEquals(Compare):
    def __init__(self, a1, a2):
        super(NotEquals, self).__init__(a1, a2)
        self.symbol = '!='

    def comp(self, v1, v2):
        return v1 != v2

    def export(self):
        return 'NotEquals(' + self._a1.export() + ',' + self._a2.export() + ')'


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
                if k1 == KEYWORD_ID:
                    p2 = namedExpr.getId()
                else:
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
                self.lenKWArgs() <= namedExpr.lenKWArgs() + 1  # les named expr de base et l'ID
        except AttributeError:
            return False

    @property
    def container(self):
        return self._getContainer()

    @abc.abstractmethod
    def _getContainer(self):
        return

    def eval(self, _, previousEvaluation):
        try:
            expressions = self.container[self.name]
        except KeyError:
            return
        for namedExpr in expressions:
            if not self.weakCompare(namedExpr):
                continue
            neval = self.unify(namedExpr, previousEvaluation)
            if neval is not None:
                yield neval

    def __hash__(self):
        return hash(self._name) + hash(self._args)

    def __eq__(self, obj):
        try:
            return self.name == obj.name and self._args == obj._args
        except AttributeError:
            return False

    def export(self):
        return self.__class__.__name__ + '(' + '\'' + str(self._name) + '\'' + \
            ',' + '[' + ','.join(arg.export() for arg in self._args) + ']' + \
            ',' + '{' + ','.join(key.export() + ':' + value.export() for key, value in self._kwargs.iteritems()) + '}' + \
            ')'


class PropertyTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(PropertyTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return Property.properties


class EventTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(EventTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return Event.events


class SpriteTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(SpriteTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return SpriteProperty.sprites


class TextTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(TextTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return TextProperty.texts


class LineTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(LineTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return LineProperty.lines


class OvalTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(OvalTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return OvalProperty.ovals


class RectTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(RectTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return RectProperty.rects


class PolygonTriggerExpression(NamedExpression):

    def __init__(self, name, args, kwargs):
        super(PolygonTriggerExpression, self).__init__(name, args, kwargs)

    def _getContainer(self):
        return PolygonProperty.polygons


class AnyEval(object):
    def __init__(self, expr):
        super(AnyEval, self).__init__()
        self._expr = expr

    def __str__(self):
        return 'AnyEval(' + str(self._expr) + ')'

    def __repr__(self):
        return 'AnyEval(' + str(self._expr) + ')'

    def eval(self, token, previousEvaluation):
        evaluations = self._expr.eval(token, previousEvaluation)
        try:
            yield evaluations.next()
        except StopIteration:
            pass

    def export(self):
        return 'AnyEval(' + self._expr.export() + ')'


class RandomEval(object):
    def __init__(self, expr):
        super(RandomEval, self).__init__()
        self._expr = expr

    def __str__(self):
        return 'RandomEval(' + str(self._expr) + ')'

    def __repr__(self):
        return 'RandomEval(' + str(self._expr) + ')'

    def eval(self, token, previousEvaluation):
        evaluations = self._expr.eval(token, previousEvaluation)

        selectedEvaluation = None

        for index, evaluation in enumerate(evaluations):
            if randint(0, index) == 0:
                selectedEvaluation = evaluation

        if selectedEvaluation is not None:
            yield selectedEvaluation

    def export(self):
        return 'RandomEval(' + self._expr.export() + ')'


class SelectEval(object):
    def __init__(self, expr, arithmExpr, selectFunction):
        super(SelectEval, self).__init__()
        self._expr = expr
        self._arithmExpr = arithmExpr
        self._selectFunction = selectFunction

    def eval(self, token, previousEvaluation):
        evaluations = self._expr.eval(token, previousEvaluation)

        selectedEvaluation = None
        selectedValue = None

        for evaluation in evaluations:
            try:
                value = self._arithmExpr.value(evaluation)

                if selectedValue is None or self._selectFunction(value, selectedValue):
                    selectedEvaluation = evaluation
                    selectedValue = value
            except (ArithmeticError, TypeError, ValueError):
                pass

        if selectedEvaluation is not None:
            yield selectedEvaluation


class SelectMinEval(SelectEval):
    def __init__(self, expr, arithmExpr):
        def selectFunction(challenger, best):
                return challenger < best
        super(SelectMinEval, self).__init__(expr, arithmExpr, selectFunction)

    def __str__(self):
        return 'SelectMinEval(' + str(self._expr) + ',' + str(self._arithmExpr) + ')'

    def __repr__(self):
        return 'SelectMinEval(' + str(self._expr) + ',' + str(self._arithmExpr) + ')'

    def export(self):
        return 'SelectMinEval(' + self._expr.export() + ',' + self._arithmExpr.export() + ')'


class SelectMaxEval(SelectEval):
    def __init__(self, expr, arithmExpr):
        def selectFunction(challenger, best):
                return challenger > best
        super(SelectMaxEval, self).__init__(expr, arithmExpr, selectFunction)

    def __str__(self):
        return 'SelectMaxEval(' + str(self._expr) + ',' + str(self._arithmExpr) + ')'

    def __repr__(self):
        return 'SelectMaxEval(' + str(self._expr) + ',' + str(self._arithmExpr) + ')'

    def export(self):
        return 'SelectMaxEval(' + self._expr.export() + ',' + self._arithmExpr.export() + ')'


class UniqueEval(object):
    def __init__(self, expr):
        super(UniqueEval, self).__init__()
        self._expr = expr

    def __str__(self):
        return 'UniqueEval(' + str(self._expr) + ')'

    def __repr__(self):
        return 'UniqueEval(' + str(self._expr) + ')'

    def eval(self, token, previousEvaluation):
        dc = DictContainer()
        for evaluation in self._expr.eval(token, previousEvaluation):
            if dc.add(evaluation.variables):
                yield evaluation

    def export(self):
        return 'UniqueEval(' + self._expr.export() + ')'