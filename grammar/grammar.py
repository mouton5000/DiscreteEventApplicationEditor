import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token
from booleanExpressions import *
from arithmeticExpressions import *


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
        iskw = Token('is')
        andkw = Token('and')
        orkw = Token('or')
        notkw = Token('not')
        elock = Keyword('eLock')

    arithmExpr = Ref('arithmExpr')
    boolExpr = Ref('boolExpr')

    litExpr = T.true | T.false
    parExpr = '(' + boolExpr + ')'

    timerExpr = T.timer + '(' + (T.integer | T.variable) + ')'
    randExpr = T.rand + '(' + (T.float | T.variable) + ')'

    eLockParameters = List(T.string | T.variable | T.integer | T.float, Token(','))
    eLockExpr = T.elock + '(' + (T.integer | T.variable) + ',' + eLockParameters + ')'

    parameters = List(T.string | T.variable | T.uvariable | T.integer | T.float, Token(','))
    propExpr = T.prop + '(' + parameters + ')'
    eventExpr = T.event + '(' + parameters + ')'

    compareArithmExpr = arithmExpr << (Token('==') | Token('>') | Token('<') | Token('<=') | Token('>=') | Token('!=')) << arithmExpr

    andExpr = boolExpr << T.andkw << boolExpr
    orExpr = boolExpr << T.orkw << boolExpr
    notExpr = T.notkw + boolExpr
    isExpr = T.variable + T.iskw + arithmExpr

    boolExpr = Prio(litExpr, timerExpr, randExpr, eLockExpr, propExpr,
                    eventExpr, parExpr, isExpr, compareArithmExpr, notExpr, andExpr, orExpr)

    addExpr = arithmExpr << (Token('+') | Token('-')) << arithmExpr
    multExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerExpr = arithmExpr << Token('**') << arithmExpr
    parArithmExpr = '(' + arithmExpr + ')'

    arithmExpr = Prio(T.integer, T.float, T.variable, parArithmExpr, powerExpr, multExpr, addExpr)

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

        def buildLitteral():
            return BLitteral(tree[1][1] == 'true')

        def buildTimer():
            nbFrames = cls.buildExpression((tree[3]))
            return Timer(nbFrames)

        def buildRand():
            prob = cls.buildExpression((tree[3]))
            return Rand(prob)

        def buildParameters():
            return [cls.buildExpression(arg) for arg in tree[1::2]]

        def buildElock():
            priority = cls.buildExpression((tree[3]))
            args = cls.buildExpression(tree[5])
            return eLock(priority, *args)

        def buildProperty():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return Property(name, *args)

        def buildEvent():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return Event(name, *args)

        def buildCompare():
            a1 = cls.buildArithmeticExpression(tree[1])
            a2 = cls.buildArithmeticExpression(tree[3])
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
            function = cls.buildArithmeticExpression(tree[3])
            return Is(variable, function)

        booleanSymbols = {
            BooleanExpressionParser.START: buildNext,
            BooleanExpressionParser.boolExpr: buildNext,
            BooleanExpressionParser.parExpr: buildDoubleNext,
            BooleanExpressionParser.T.event: value,
            BooleanExpressionParser.T.prop: value,
            BooleanExpressionParser.T.variable: value,
            BooleanExpressionParser.T.uvariable: value,
            BooleanExpressionParser.T.string: stringWithoutQuotes,
            BooleanExpressionParser.T.integer: intvalue,
            BooleanExpressionParser.T.float: floatvalue,
            BooleanExpressionParser.litExpr: buildLitteral,
            BooleanExpressionParser.timerExpr: buildTimer,
            BooleanExpressionParser.randExpr: buildRand,
            BooleanExpressionParser.parameters: buildParameters,
            BooleanExpressionParser.eLockParameters: buildParameters,
            BooleanExpressionParser.eLockExpr: buildElock,
            BooleanExpressionParser.propExpr: buildProperty,
            BooleanExpressionParser.eventExpr: buildEvent,
            BooleanExpressionParser.compareArithmExpr: buildCompare,
            BooleanExpressionParser.andExpr: buildAnd,
            BooleanExpressionParser.orExpr: buildOr,
            BooleanExpressionParser.notExpr: buildNot,
            BooleanExpressionParser.isExpr: buildIs

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
            BooleanExpressionParser.addExpr: buildBinaryExpression,
            BooleanExpressionParser.multExpr: buildBinaryExpression,
            BooleanExpressionParser.powerExpr: buildBinaryExpression
        }

        return arithmeticSymbols[rootName]()

if __name__ == '__main__':
    exprToPars = 'pW(X,Y) and (eLock(6,X,Y) or eLock(4,X,Y))'
    b = BExpression(BooleanExpressionParser.parse(exprToPars))

    Property.properties = [Property('W', 0, 0), Property('W', 0, 1), Property('W', 1, 0), Property('W', 1, 1)]+\
                          [Property('S', 0, 0), Property('S', 0, 2), Property('S', 0, 0), Property('S', 2, 2)]
    print b
    for e in b.eval():
        print e