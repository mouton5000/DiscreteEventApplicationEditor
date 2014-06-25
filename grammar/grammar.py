import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token, Opt
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, Power
from booleanExpressions import BLitteral, Timer, Rand, RandInt, eLock, PropertyBooleanExpression, \
    EventBooleanExpression, TokenExpression, Equals, GreaterThan, LowerThan, GeqThan, LeqThan, \
    NotEquals, And, Or, Not, Is
from database import Variable


class BooleanExpressionParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='[0-9]+')
        float = Token(re='[0-9]+\.[0-9]+')
        string = Token(re='\'[A-Za-z_0-9]*\'')
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
    randIntExpr = T.randInt + '(' + Prio(T.variable, arithmExpr) + ',' + T.integer + ')'

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

    addExpr = arithmExpr << Token('+') << arithmExpr
    minusExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerExpr = arithmExpr << Token('**') << arithmExpr
    parArithmExpr = '(' + arithmExpr + ')'

    arithmExpr = Prio(T.integer, T.float, T.variable, T.string, parArithmExpr, powerExpr, multExpr, addExpr, minusExpr)

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

        def stringWithoutQuotes():
            return tree[1][1:-1]

        def intvalue():
            return int(tree[1])

        def floatvalue():
            return float(tree[1])

        def variableValue():
            return Variable(tree[1])

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
            return eLock(priority, *args)

        def buildProperty():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return PropertyBooleanExpression(name, *args)

        def buildEvent():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return EventBooleanExpression(name, *args)

        def buildToken():
            args = cls.buildExpression(tree[3])
            return TokenExpression(*args)

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
            BooleanExpressionParser.T.uvariable: variableValue,
            BooleanExpressionParser.T.string: stringWithoutQuotes,
            BooleanExpressionParser.T.integer: intvalue,
            BooleanExpressionParser.T.float: floatvalue,
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

        def buildNext():
            return cls.buildArithmeticExpression(tree[1])

        def buildDoubleNext():
            return cls.buildArithmeticExpression(tree[2])

        def buildLitteral():
            return ALitteral(cls.buildExpression(tree))

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

        arithmeticSymbols = {
            BooleanExpressionParser.arithmExpr: buildNext,
            BooleanExpressionParser.parArithmExpr: buildDoubleNext,
            BooleanExpressionParser.T.integer: buildLitteral,
            BooleanExpressionParser.T.float: buildLitteral,
            BooleanExpressionParser.T.variable: buildLitteral,
            BooleanExpressionParser.T.string: buildLitteral,
            BooleanExpressionParser.addExpr: buildBinaryExpression,
            BooleanExpressionParser.minusExpr: buildMinusExpression,
            BooleanExpressionParser.multExpr: buildBinaryExpression,
            BooleanExpressionParser.powerExpr: buildBinaryExpression
        }

        return arithmeticSymbols[rootName]()

if __name__ == '__main__':
    expr = 'eLock(\'move\',-X)'
    expr = BooleanExpressionParser.parse(expr)
    for evaluation in expr.eval(1, {Variable('X'):1}):
        print evaluation