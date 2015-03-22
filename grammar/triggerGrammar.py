import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token, Opt
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, \
    Power, Func, UndefinedLitteral, Min, Max
from triggerExpressions import BLitteral, Timer, Rand, RandInt, eLock, PropertyBooleanExpression, \
    EventBooleanExpression, TokenExpression, Equals, GreaterThan, LowerThan, GeqThan, LeqThan, \
    NotEquals, And, Or, Not, Is
from database import Variable
from utils.mathutils import sign
from math import cos, sin, tan, exp, log, floor, ceil, acos, asin, atan, cosh, sinh, tanh, acosh, atanh, asinh


class TriggerParser(lrparsing.Grammar):
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

        cosf = Token('cos')
        sinf = Token('sin')
        tanf = Token('tan')
        expf = Token('exp')
        logf = Token('log')
        absf = Token('abs')
        signf = Token('sign')
        floorf = Token('floor')
        ceilf = Token('ceil')
        acosf = Token('acos')
        asinf = Token('asin')
        atanf = Token('atan')
        chf = Token('ch')
        shf = Token('sh')
        thf = Token('th')
        achf = Token('ach')
        ashf = Token('ash')
        athf = Token('ath')

        lenf = Token('len')

        minf = Token('min')
        maxf = Token('max')

    arithmExpr = Ref('arithmExpr')
    boolExpr = Ref('boolExpr')

    litExpr = T.true | T.false
    parExpr = '(' + boolExpr + ')'

    timerExpr = T.timer + '(' + arithmExpr + ')'
    randExpr = T.rand + '(' + arithmExpr + ')'
    randIntExpr = T.randInt + '(' + Prio(T.variable, arithmExpr) + ',' + arithmExpr + ')'

    eLockParameters = List(arithmExpr, Token(','))
    eLockExpr = T.elock + '(' + arithmExpr + ',' + eLockParameters + ')'

    parameter = Prio(T.variable, arithmExpr) | T.uvariable
    namedParameter = arithmExpr + '=' + parameter
    parameters = \
        Prio(List(parameter, Token(',')) + Opt(',' + List(namedParameter, Token(','))),
             List(namedParameter, Token(',')))
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

    # listExpr = '[' + List(arithmExpr, Token(',')) + ']'
    # linkedListExpr = 'll' + listExpr
    # setExpr = 'set' + listExpr

    addExpr = arithmExpr << Token('+') << arithmExpr
    minusExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerExpr = arithmExpr << Token('**') << arithmExpr
    constantExpr = Token('pi') | Token('e')
    parArithmExpr = '(' + arithmExpr + ')'

    unaryFuncExpr = (T.cosf | T.sinf | T.tanf | T.expf | T.logf | T.absf | T.signf | T.floorf | T.ceilf
                     | T.acosf | T.asinf | T.atanf | T.shf | T.chf | T.thf | T.ashf | T.achf | T.athf | T.lenf) \
                     + parArithmExpr
    binaryFuncExpr = (T.minf | T.maxf) + '(' + arithmExpr + ',' + arithmExpr + ')'

    # getItemExpr = arithmExpr + '[' + arithmExpr + ']'
    # setItemExpr = arithmExpr + '[' + arithmExpr + '<<' + arithmExpr + ']'
    # insertExpr = T.insertf + '(' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ')'
    # popExpr = T.popf + '(' + arithmExpr + Opt(',' + arithmExpr) + ')'
    # getSublistExpr = arithmExpr + '[' + Opt(arithmExpr) + ':' + Opt(arithmExpr) + ']'
    # insertExpr = T.insertf + '(' + arithmExpr + ',' + arithmExpr + ',' + Opt(arithmExpr) + ')'
    # removeExpr = T.popf + '(' + arithmExpr << '>' << ((arithmExpr << '>') | ('>' << Opt('>') << arithmExpr))

    arithmExpr = Prio(T.integer, T.float, T.variable, T.string, constantExpr,
                      # listExpr,
                      # linkedListExpr,
                      # setExpr,
                      parArithmExpr,
                      # getItemExpr, getSublistExpr, insertExpr, removeExpr,
                      unaryFuncExpr, binaryFuncExpr, powerExpr, multExpr, minusExpr, addExpr)

    START = boolExpr

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(TriggerParser, cls).parse(expr, tree_factory, on_error, log)
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
            return UndefinedLitteral()

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

        def buildNamedParameter():
            name = cls.buildExpression(tree[1])
            parameter = cls.buildExpression(tree[3])
            return name, parameter

        def buildParameters():
            buildArgs = [cls.buildExpression(arg) for arg in tree[1::2]]
            args = [arg for arg in buildArgs if not isinstance(arg, tuple)]
            kwargs = {kwarg[0]: kwarg[1] for kwarg in buildArgs if isinstance(kwarg, tuple)}
            return args, kwargs

        def buildELockParameters():
            return [cls.buildExpression(arg) for arg in tree[1::2]]

        def buildElock():
            priority = cls.buildExpression(tree[3])
            args = cls.buildExpression(tree[5])
            return eLock(priority, args)

        def buildProperty():
            name = cls.buildExpression(tree[1])[1:]
            args, kwargs = cls.buildExpression(tree[3])
            return PropertyBooleanExpression(name, args, kwargs)

        def buildEvent():
            name = cls.buildExpression(tree[1])[1:]
            args, kwargs = cls.buildExpression(tree[3])
            return EventBooleanExpression(name, args, kwargs)

        def buildToken():
            args, kwargs = cls.buildExpression(tree[3])
            return TokenExpression(args, kwargs)

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
            TriggerParser.START: buildNext,
            TriggerParser.boolExpr: buildNext,
            TriggerParser.parExpr: buildDoubleNext,
            TriggerParser.T.event: value,
            TriggerParser.T.prop: value,
            TriggerParser.T.variable: variableValue,
            TriggerParser.T.uvariable: unnamedVariableValue,
            TriggerParser.litExpr: buildLitteral,
            TriggerParser.timerExpr: buildTimer,
            TriggerParser.randExpr: buildRand,
            TriggerParser.randIntExpr: buildRandInt,
            TriggerParser.parameter: buildNext,
            TriggerParser.namedParameter: buildNamedParameter,
            TriggerParser.parameters: buildParameters,
            TriggerParser.eLockParameters: buildELockParameters,
            TriggerParser.eLockExpr: buildElock,
            TriggerParser.propExpr: buildProperty,
            TriggerParser.eventExpr: buildEvent,
            TriggerParser.tokenExpr: buildToken,
            TriggerParser.compareArithmExpr: buildCompare,
            TriggerParser.andExpr: buildAnd,
            TriggerParser.orExpr: buildOr,
            TriggerParser.notExpr: buildNot,
            TriggerParser.isExpr: buildIs,
            TriggerParser.arithmExpr: buildArithmetic
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

        # def listValue():
        #     args = [cls.buildArithmeticExpression(arg) for arg in tree[2:-1:2]]
        #     return ListLitteral(args)
        #
        # def linkedListValue():
        #     args = [cls.buildArithmeticExpression(arg) for arg in tree[2][2:-1:2]]
        #     return LinkedListLitteral(args)
        #
        # def setValue():
        #     args = [cls.buildArithmeticExpression(arg) for arg in tree[2][2:-1:2]]
        #     return SetLitteral(args)
        #
        # def buildGetItemExpression():
        #     l1 = cls.buildArithmeticExpression(tree[1])
        #     a2 = cls.buildArithmeticExpression(tree[3])
        #     return GetItemExpression(l1, a2)
        #
        # def buildGetSublistExpression():
        #     l1 = cls.buildArithmeticExpression(tree[1])
        #     s = len(tree)
        #     if s == 7:
        #         a1 = cls.buildArithmeticExpression(tree[3])
        #         a2 = cls.buildArithmeticExpression(tree[5])
        #     elif s == 5:
        #         a1 = None
        #         a2 = None
        #     elif tree[3][1] == ':':
        #         a1 = None
        #         a2 = cls.buildArithmeticExpression(tree[4])
        #     else:
        #         a1 = cls.buildArithmeticExpression(tree[3])
        #         a2 = None
        #     return GetSublistExpression(l1, a1, a2)
        #
        # def buildInsertExpression():
        #     l1 = cls.buildArithmeticExpression(tree[1])
        #     a2 = cls.buildArithmeticExpression(tree[-1])
        #     s = len(tree)
        #     if s == 6:
        #         a1 = cls.buildArithmeticExpression(tree[3])
        #     else:
        #         a1 = None
        #     return InsertExpression(l1, a1, a2)
        #
        # def buildRemoveExpression():
        #     l1 = cls.buildArithmeticExpression(tree[1])
        #     s = len(tree)
        #     if s == 6:
        #         a2 = cls.buildArithmeticExpression(tree[-1])
        #         return RemoveAllExpression(l1, a2)
        #     else:
        #         if tree[3][1] == '>':
        #             a2 = cls.buildArithmeticExpression(tree[-1])
        #             return RemoveExpression(l1, None, a2)
        #         else:
        #             a1 = cls.buildArithmeticExpression(tree[3])
        #             return RemoveExpression(l1, a1, None)

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

        def buildUnaryFunctionExpression():
            a = cls.buildArithmeticExpression(tree[2])
            if tree[1][1] == 'cos':
                return Func(a, cos)
            elif tree[1][1] == 'sin':
                return Func(a, sin)
            elif tree[1][1] == 'tan':
                return Func(a, tan)
            elif tree[1][1] == 'acos':
                return Func(a, acos)
            elif tree[1][1] == 'asin':
                return Func(a, asin)
            elif tree[1][1] == 'atan':
                return Func(a, atan)
            elif tree[1][1] == 'ch':
                return Func(a, cosh)
            elif tree[1][1] == 'sh':
                return Func(a, sinh)
            elif tree[1][1] == 'th':
                return Func(a, tanh)
            elif tree[1][1] == 'ash':
                return Func(a, acosh)
            elif tree[1][1] == 'ash':
                return Func(a, asinh)
            elif tree[1][1] == 'ath':
                return Func(a, atanh)
            elif tree[1][1] == 'exp':
                return Func(a, exp)
            elif tree[1][1] == 'log':
                return Func(a, log)
            elif tree[1][1] == 'abs':
                return Func(a, abs)
            elif tree[1][1] == 'sign':
                return Func(a, sign)
            elif tree[1][1] == 'ceil':
                return Func(a, ceil)
            elif tree[1][1] == 'floor':
                return Func(a, floor)
            elif tree[1][1] == 'len':
                return Func(a, len)

        def buildBinaryFunctionExpression():
            x1 = cls.buildArithmeticExpression(tree[3])
            x2 = cls.buildArithmeticExpression(tree[5])
            if tree[1][1] == 'min':
                return Min(x1, x2)
            elif tree[1][1] == 'max':
                return Max(x1, x2)

        arithmeticSymbols = {
            TriggerParser.arithmExpr: buildNext,
            TriggerParser.parArithmExpr: buildDoubleNext,
            TriggerParser.T.integer: intvalue,
            TriggerParser.T.float: floatvalue,
            TriggerParser.T.variable: variableValue,
            TriggerParser.T.string: stringWithoutQuotes,
            # TriggerParser.listExpr: listValue,
            # TriggerParser.linkedListExpr: linkedListValue,
            # TriggerParser.setExpr: setValue,
            # TriggerParser.getItemExpr: buildGetItemExpression,
            # TriggerParser.getSublistExpr: buildGetSublistExpression,
            # TriggerParser.insertExpr: buildInsertExpression,
            # TriggerParser.removeExpr: buildRemoveExpression,
            TriggerParser.addExpr: buildBinaryExpression,
            TriggerParser.minusExpr: buildMinusExpression,
            TriggerParser.multExpr: buildBinaryExpression,
            TriggerParser.powerExpr: buildBinaryExpression,
            TriggerParser.constantExpr: buildConstant,
            TriggerParser.unaryFuncExpr: buildUnaryFunctionExpression,
            TriggerParser.binaryFuncExpr: buildBinaryFunctionExpression
        }

        return arithmeticSymbols[rootName]()

if __name__ == '__main__':
    # print BooleanExpressionParser.pre_compile_grammar()
    expr = 'pTest(X,Y, Z = 2, \'abc\' = X + 2, 2 + 4 - Z =Y)'
    expr = TriggerParser.parse(expr)
    print expr