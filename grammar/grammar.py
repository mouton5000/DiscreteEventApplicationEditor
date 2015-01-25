import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token, Opt
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, \
    Power, Func, ListLitteral, LinkedListLitteral, SetLitteral, GetItemExpression, GetSublistExpression, \
    InsertExpression, RemoveAllExpression, RemoveExpression, UndefinnedLitteral
from booleanExpressions import BLitteral, Timer, Rand, RandInt, eLock, PropertyBooleanExpression, \
    EventBooleanExpression, TokenExpression, Equals, GreaterThan, LowerThan, GeqThan, LeqThan, \
    NotEquals, And, Or, Not, Is
from database import Variable


class BooleanExpressionParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='[0-9]+')
        float = Token(re='[0-9]+\.[0-9]+')
        string = Token(re='\'[^\']*\'')
        prop = Token(re='p[A-Z][A-Za-z_0-9]*')
        event = Token(re='e[A-Z][A-Za-z_0-9]*')
        variable = Token(re='[A-Z][A-Z_0-9]*')
        uvariable = Token('_')
        true = Token('true')
        false = Token('false')
        timer = Token('timer')
        rand = Token('rand')
        randInt = Token('randInt')
        iskw = Token('is')
        andkw = Token('and')
        orkw = Token('or')
        notkw = Token('not')
        token = Token('token')
        elock = Keyword('eLock')

    arithmExpr = Ref('arithmExpr')
    boolExpr = Ref('boolExpr')

    litExpr = T.true | T.false
    parExpr = '(' + boolExpr + ')'

    timerExpr = T.timer + '(' + arithmExpr + ')'
    randExpr = T.rand + '(' + arithmExpr + ')'
    randIntExpr = T.randInt + '(' + Prio(T.variable, arithmExpr) + ',' + arithmExpr + ')'

    eLockParameters = List(arithmExpr, Token(','))
    eLockExpr = T.elock + '(' + arithmExpr + ',' + eLockParameters + ')'

    parameters = List(Prio(T.variable, arithmExpr) | T.uvariable, Token(','))
    propExpr = T.prop + '(' + parameters + ')'
    eventExpr = T.event + '(' + parameters + ')'
    tokenExpr = T.token + '(' + parameters + ')'

    compareArithmExpr = arithmExpr << (Token('==') | Token('>') | Token('<') | Token('<=') |
                                       Token('>=') | Token('!=')) << arithmExpr

    andExpr = boolExpr << T.andkw << boolExpr
    orExpr = boolExpr << T.orkw << boolExpr
    notExpr = T.notkw + boolExpr
    isExpr = T.variable + T.iskw + arithmExpr

    boolExpr = Prio(litExpr, timerExpr, randExpr, randIntExpr, eLockExpr, propExpr,
                    eventExpr, tokenExpr, parExpr, isExpr, compareArithmExpr, notExpr, andExpr, orExpr)

    listExpr = '[' + List(arithmExpr, Token(',')) + ']'
    linkedListExpr = 'll' + listExpr
    setExpr = 'set' + listExpr

    addExpr = arithmExpr << Token('+') << arithmExpr
    minusExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerExpr = arithmExpr << Token('**') << arithmExpr
    constantExpr = Token('pi') | Token('e')
    parArithmExpr = '(' + arithmExpr + ')'
    funcExpr = (Token('cos') | Token('sin') | Token('tan') | Token('exp') | Token('log') | Token('abs') |
                Token('sign') | Token('floor') | Token('ceil') | Token('acos') | Token('asin') | Token('atan') |
                Token('sh') | Token('ch') | Token('th') | Token('ash') | Token('ach') | Token('ath') | Token('len')) \
               + parArithmExpr
    getItemExpr = arithmExpr + '[' + arithmExpr + ']'
    getSublistExpr = arithmExpr + '[' + Opt(arithmExpr) + ':' + Opt(arithmExpr) + ']'
    insertExpr = arithmExpr << '<' << Opt(arithmExpr) << '<' << arithmExpr
    removeExpr = arithmExpr << '>' << ((arithmExpr << '>') | ('>' << Opt('>') << arithmExpr))

    arithmExpr = Prio(T.integer, T.float, T.variable, T.string, constantExpr, listExpr, linkedListExpr,
                      setExpr, parArithmExpr, getItemExpr, getSublistExpr, insertExpr, removeExpr,
                      funcExpr, powerExpr, multExpr, addExpr, minusExpr)

    START = boolExpr

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(BooleanExpressionParser, cls).parse(expr, tree_factory, on_error, log)
        return cls.buildExpression(tree)

    @classmethod
    def buildExpression(cls, tree):
        rootName = tree[0]

        def buildNext():
            return cls.buildExpression(tree[1])

        def buildDoubleNext():
            return cls.buildExpression(tree[2])

        def value():
            return tree[1]

        def variableValue():
            return Variable(tree[1])

        def unnamedVariableValue():
            return UndefinnedLitteral()

        def buildLitteral():
            return BLitteral(tree[1][1] == 'true')

        def buildTimer():
            nbFrames = cls.buildExpression((tree[3]))
            return Timer(nbFrames)

        def buildRand():
            prob = cls.buildExpression((tree[3]))
            return Rand(prob)

        def buildRandInt():
            var = cls.buildExpression((tree[3]))
            max = cls.buildExpression((tree[5]))
            return RandInt(var, max)

        def buildParameters():
            return [cls.buildExpression(arg) for arg in tree[1::2]]

        def buildElock():
            priority = cls.buildExpression(tree[3])
            args = cls.buildExpression(tree[5])
            return eLock(priority, args)

        def buildProperty():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return PropertyBooleanExpression(name, args)

        def buildEvent():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return EventBooleanExpression(name, args)

        def buildToken():
            args = cls.buildExpression(tree[3])
            return TokenExpression(args)

        def buildCompare():
            a1 = cls.buildExpression(tree[1])
            a2 = cls.buildExpression(tree[3])
            if tree[2][1] == '==':
                return Equals(a1, a2)
            elif tree[2][1] == '>':
                return GreaterThan(a1, a2)
            elif tree[2][1] == '<':
                return LowerThan(a1, a2)
            elif tree[2][1] == '>=':
                return GeqThan(a1, a2)
            elif tree[2][1] == '<=':
                return LeqThan(a1, a2)
            elif tree[2][1] == '!=':
                return NotEquals(a1, a2)

        def buildAnd():
            a1 = cls.buildExpression((tree[1]))
            a2 = cls.buildExpression((tree[3]))
            return And(a1, a2)

        def buildOr():
            a1 = cls.buildExpression((tree[1]))
            a2 = cls.buildExpression((tree[3]))
            return Or(a1, a2)

        def buildNot():
            a1 = cls.buildExpression((tree[2]))
            return Not(a1)

        def buildIs():
            variable = cls.buildExpression(tree[1])
            function = cls.buildExpression(tree[3])
            return Is(variable, function)

        def buildArithmetic():
            return cls.buildArithmeticExpression(tree)

        booleanSymbols = {
            BooleanExpressionParser.START: buildNext,
            BooleanExpressionParser.boolExpr: buildNext,
            BooleanExpressionParser.parExpr: buildDoubleNext,
            BooleanExpressionParser.T.event: value,
            BooleanExpressionParser.T.prop: value,
            BooleanExpressionParser.T.variable: variableValue,
            BooleanExpressionParser.T.uvariable: unnamedVariableValue,
            BooleanExpressionParser.litExpr: buildLitteral,
            BooleanExpressionParser.timerExpr: buildTimer,
            BooleanExpressionParser.randExpr: buildRand,
            BooleanExpressionParser.randIntExpr: buildRandInt,
            BooleanExpressionParser.parameters: buildParameters,
            BooleanExpressionParser.eLockParameters: buildParameters,
            BooleanExpressionParser.eLockExpr: buildElock,
            BooleanExpressionParser.propExpr: buildProperty,
            BooleanExpressionParser.eventExpr: buildEvent,
            BooleanExpressionParser.tokenExpr: buildToken,
            BooleanExpressionParser.compareArithmExpr: buildCompare,
            BooleanExpressionParser.andExpr: buildAnd,
            BooleanExpressionParser.orExpr: buildOr,
            BooleanExpressionParser.notExpr: buildNot,
            BooleanExpressionParser.isExpr: buildIs,
            BooleanExpressionParser.arithmExpr: buildArithmetic

        }

        return booleanSymbols[rootName]()

    @classmethod
    def buildArithmeticExpression(cls, tree):
        rootName = tree[0]

        def stringWithoutQuotes():
            return ALitteral(tree[1][1:-1])

        def intvalue():
            return ALitteral(int(tree[1]))

        def floatvalue():
            return ALitteral(float(tree[1]))

        def variableValue():
            return ALitteral(Variable(tree[1]))

        def listValue():
            args = [cls.buildArithmeticExpression(arg) for arg in tree[2:-1:2]]
            return ListLitteral(args)

        def linkedListValue():
            args = [cls.buildArithmeticExpression(arg) for arg in tree[2][2:-1:2]]
            return LinkedListLitteral(args)

        def setValue():
            args = [cls.buildArithmeticExpression(arg) for arg in tree[2][2:-1:2]]
            return SetLitteral(args)

        def buildGetItemExpression():
            l1 = cls.buildArithmeticExpression(tree[1])
            a2 = cls.buildArithmeticExpression(tree[3])
            return GetItemExpression(l1, a2)

        def buildGetSublistExpression():
            l1 = cls.buildArithmeticExpression(tree[1])
            s = len(tree)
            if s == 7:
                a1 = cls.buildArithmeticExpression(tree[3])
                a2 = cls.buildArithmeticExpression(tree[5])
            elif s == 5:
                a1 = None
                a2 = None
            elif tree[3][1] == ':':
                a1 = None
                a2 = cls.buildArithmeticExpression(tree[4])
            else:
                a1 = cls.buildArithmeticExpression(tree[3])
                a2 = None
            return GetSublistExpression(l1, a1, a2)

        def buildInsertExpression():
            l1 = cls.buildArithmeticExpression(tree[1])
            a2 = cls.buildArithmeticExpression(tree[-1])
            s = len(tree)
            if s == 6:
                a1 = cls.buildArithmeticExpression(tree[3])
            else:
                a1 = None
            return InsertExpression(l1, a1, a2)

        def buildRemoveExpression():
            l1 = cls.buildArithmeticExpression(tree[1])
            s = len(tree)
            if s == 6:
                a2 = cls.buildArithmeticExpression(tree[-1])
                return RemoveAllExpression(l1, a2)
            else:
                if tree[3][1] == '>':
                    a2 = cls.buildArithmeticExpression(tree[-1])
                    return RemoveExpression(l1, None, a2)
                else:
                    a1 = cls.buildArithmeticExpression(tree[3])
                    return RemoveExpression(l1, a1, None)

        def buildNext():
            return cls.buildArithmeticExpression(tree[1])

        def buildDoubleNext():
            return cls.buildArithmeticExpression(tree[2])

        def buildConstant():
            from math import pi, e
            if tree[1][1] == 'pi':
                value = pi
            else:
                value = e
            return ALitteral(value)

        def buildMinusExpression():
            if len(tree) == 4:
                return buildBinaryExpression()
            else:
                a1 = cls.buildArithmeticExpression(tree[2])
                return Subtraction(ALitteral(0), a1)

        def buildBinaryExpression():
            a1 = cls.buildArithmeticExpression(tree[1])
            a3 = cls.buildArithmeticExpression(tree[3])
            if tree[2][1] == '+':
                return Addition(a1, a3)
            elif tree[2][1] == '-':
                return Subtraction(a1, a3)
            elif tree[2][1] == '*':
                return Product(a1, a3)
            elif tree[2][1] == '/':
                return Division(a1, a3)
            elif tree[2][1] == '//':
                return EuclideanDivision(a1, a3)
            elif tree[2][1] == '%':
                return Modulo(a1, a3)
            elif tree[2][1] == '**':
                return Power(a1, a3)

        def buildFunctionExpression():
            a = cls.buildArithmeticExpression(tree[2])
            if tree[1][1] == 'cos':
                from math import cos
                return Func(a, cos)
            elif tree[1][1] == 'sin':
                from math import sin
                return Func(a, sin)
            elif tree[1][1] == 'tan':
                from math import tan
                return Func(a, tan)
            elif tree[1][1] == 'acos':
                from math import acos
                return Func(a, acos)
            elif tree[1][1] == 'asin':
                from math import asin
                return Func(a, asin)
            elif tree[1][1] == 'atan':
                from math import atan
                return Func(a, atan)
            elif tree[1][1] == 'ch':
                from math import acosh
                return Func(a, acosh)
            elif tree[1][1] == 'sh':
                from math import asinh
                return Func(a, asinh)
            elif tree[1][1] == 'th':
                from math import atanh
                return Func(a, atanh)
            elif tree[1][1] == 'cosh':
                from math import cosh
                return Func(a, cosh)
            elif tree[1][1] == 'sinh':
                from math import sinh
                return Func(a, sinh)
            elif tree[1][1] == 'tanh':
                from math import tanh
                return Func(a, tanh)
            elif tree[1][1] == 'exp':
                from math import exp
                return Func(a, exp)
            elif tree[1][1] == 'log':
                from math import log
                return Func(a, log)
            elif tree[1][1] == 'abs':
                return Func(a, abs)
            elif tree[1][1] == 'sign':
                def sign(x):
                    if x == 0:
                        return 0
                    elif x > 0:
                        return 1
                    else:
                        return -1
                return Func(a, sign)
            elif tree[1][1] == 'ceil':
                from math import ceil
                return Func(a, ceil)
            elif tree[1][1] == 'floor':
                from math import floor
                return Func(a, floor)
            elif tree[1][1] == 'len':
                return Func(a, len)

        arithmeticSymbols = {
            BooleanExpressionParser.arithmExpr: buildNext,
            BooleanExpressionParser.parArithmExpr: buildDoubleNext,
            BooleanExpressionParser.T.integer: intvalue,
            BooleanExpressionParser.T.float: floatvalue,
            BooleanExpressionParser.T.variable: variableValue,
            BooleanExpressionParser.T.string: stringWithoutQuotes,
            BooleanExpressionParser.listExpr: listValue,
            BooleanExpressionParser.linkedListExpr: linkedListValue,
            BooleanExpressionParser.setExpr: setValue,
            BooleanExpressionParser.getItemExpr: buildGetItemExpression,
            BooleanExpressionParser.getSublistExpr: buildGetSublistExpression,
            BooleanExpressionParser.insertExpr: buildInsertExpression,
            BooleanExpressionParser.removeExpr: buildRemoveExpression,
            BooleanExpressionParser.addExpr: buildBinaryExpression,
            BooleanExpressionParser.minusExpr: buildMinusExpression,
            BooleanExpressionParser.multExpr: buildBinaryExpression,
            BooleanExpressionParser.powerExpr: buildBinaryExpression,
            BooleanExpressionParser.constantExpr: buildConstant,
            BooleanExpressionParser.funcExpr: buildFunctionExpression
        }

        return arithmeticSymbols[rootName]()

if __name__ == '__main__':
    print BooleanExpressionParser.pre_compile_grammar()
    expr = 'X is [1,2,5,4,5,6] and randInt(I, len(X))'
    expr = BooleanExpressionParser.parse(expr)
    for evaluation in expr.eval(1, {Variable('Y'): 1}):
        print evaluation
