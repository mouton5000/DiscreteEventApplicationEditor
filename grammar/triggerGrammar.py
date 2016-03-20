import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token, Opt
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, \
    Power, Func, UndefinedLitteral, Min, Max, globalsHeightExpression, globalsWidthExpression, globalsFpsExpression
from triggerExpressions import BLitteral, Timer, eLock, \
    Equals, GreaterThan, LowerThan, GeqThan, LeqThan, \
    NotEquals, And, Or, Not, Is, AnyEval, RandomEval, Del, \
    SelectMinEval, SelectMaxEval, UniqueEval, PropertyTriggerExpression, \
    EventTriggerExpression, SpriteTriggerExpression, TextTriggerExpression, \
    LineTriggerExpression, OvalTriggerExpression, RectTriggerExpression, PolygonTriggerExpression
from database import Variable
from keywords import KEYWORD_ID, KEYWORD_FILENAME, KEYWORD_COLOR, KEYWORD_FONT_NAME, KEYWORD_FONT_SIZE, KEYWORD_H, \
    KEYWORD_TEXT, KEYWORD_WIDTH, KEYWORD_W, KEYWORD_X_INT, KEYWORD_X, KEYWORD_Y_INT, KEYWORD_Y, KEYWORD_Z, \
    KEYWORD_ROTATE, KEYWORD_SCALE
from utils.mathutils import sign
from random import random, randint
from math import cos, sin, tan, exp, log, floor, ceil, acos, asin, atan, cosh, sinh, tanh, acosh, atanh, asinh


class TriggerParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='[0-9]+')
        float = Token(re='[0-9]+\.[0-9]+')
        string = Token(re='\'[^\']*\'')
        true = Token('true')
        false = Token('false')

        variable = Token(re='[A-Z][A-Z_0-9]*')
        uvariable = Token('_')

        prop = Token(re='p[A-Z][A-Za-z_0-9]*')
        event = Token(re='e[A-Z][A-Za-z_0-9]*')
        graphicsSprite = Token(re='gs[A-Z][A-Za-z_0-9]*')
        graphicsLine = Token(re='gl[A-Z][A-Za-z_0-9]*')
        graphicsOval = Token(re='go[A-Z][A-Za-z_0-9]*')
        graphicsRect = Token(re='gr[A-Z][A-Za-z_0-9]*')
        graphicsPolygon = Token(re='gp[A-Z][A-Za-z_0-9]*')
        graphicsText = Token(re='gt[A-Z][A-Za-z_0-9]*')

        idkw = Token('id')

        coordX = Token('x')
        coordY = Token('y')
        coordZ = Token('z')
        coordXInt = Token(re='x[1-9][0-9]*')
        coordYInt = Token(re='y[1-9][0-9]*')
        coordW = Token('w')
        coordH = Token('h')
        rotate = Token('rotate')
        scale = Token('scale')

        fileName = Token('fileName')
        color = Token('color')
        width = Token('width')
        text = Token('text')
        fontName = Token('fontName')
        fontSize = Token('fontSize')

        cosf = Token('cos')
        sinf = Token('sin')
        tanf = Token('tan')
        expf = Token('exp')
        logf = Token('log')
        absf = Token('abs')
        signf = Token('sign')
        floorf = Token('floor')
        ceilf = Token('ceil')
        roundf = Token('round')
        acosf = Token('acos')
        asinf = Token('asin')
        atanf = Token('atan')
        chf = Token('ch')
        shf = Token('sh')
        thf = Token('th')
        achf = Token('ach')
        ashf = Token('ash')
        athf = Token('ath')
        rand = Token('rand')
        randint = Token('randint')

        lenf = Token('len')
        minf = Token('min')
        maxf = Token('max')

        globalsKw = Token('globals')
        globalsFpsKw = Token('fps')
        globalsHeightKw = Token('screenHeight')
        globalsWidthKw = Token('screenWidth')

        elock = Keyword('eLock')
        timer = Token('timer')
        iskw = Token('is')
        delkw = Token('del')
        andkw = Token('and')
        orkw = Token('or')
        notkw = Token('not')

        anyEval = Token('anyEval')
        randomEval = Token('randomEval')
        minEvalKw = Token('minEval')
        maxEvalKw = Token('maxEval')
        uniqueEval = Token('uniqueEval')

    arithmExpr = Ref('arithmExpr')
    boolExpr = Ref('boolExpr')

    litExpr = T.true | T.false

    timerExpr = T.timer + '(' + arithmExpr + ')'

    eLockParameters = List(arithmExpr, Token(','), min=1)
    eLockExpr = T.elock + '(' + arithmExpr + Opt(',' + eLockParameters) + ')'

    parameter = Prio(T.variable, arithmExpr) | T.uvariable

    namedParameterKW = arithmExpr | T.idkw | \
                       T.coordX | T.coordY | T.coordZ | \
                       T.coordXInt | T.coordYInt | \
                       T.coordH | T.coordW | \
                       T.rotate | T.scale | \
                       T.fileName | \
                       T.color | T.width | \
                       T.text | T.fontName | T.fontSize
    namedParameter = namedParameterKW + '=' + parameter
    parameters = \
        Prio(List(parameter, Token(',')) + Opt(',' + List(namedParameter, Token(','))),
             List(namedParameter, Token(',')))

    parameterizedType = T.prop | T.event | T.graphicsSprite | T.graphicsText | T.graphicsLine | \
                        T.graphicsOval | T.graphicsRect | T.graphicsPolygon
    parameterizedExpr = parameterizedType + '(' + parameters + ')'

    compareArithmExpr = arithmExpr << (Token('==') | Token('>') | Token('<') | Token('<=') |
                                       Token('>=') | Token('!=')) << arithmExpr

    andExpr = boolExpr >> T.andkw >> boolExpr
    orExpr = boolExpr >> T.orkw >> boolExpr
    notExpr = T.notkw + boolExpr
    isExpr = T.variable + T.iskw + arithmExpr
    delExpr = T.delkw + T.variable

    parExpr = '(' + boolExpr + ')'

    anyEvalExpr = T.anyEval + parExpr
    randomEvalExpr = T.randomEval + parExpr
    minEvalExpr = T.minEvalKw + '[' + arithmExpr + ']' + parExpr
    maxEvalExpr = T.maxEvalKw + '[' + arithmExpr + ']' + parExpr
    uniqueEvalExpr = T.uniqueEval + parExpr

    boolExpr = Prio(litExpr,
                    timerExpr,
                    eLockExpr,
                    parameterizedExpr,
                    parExpr,
                    isExpr,
                    delExpr,
                    compareArithmExpr,
                    notExpr,
                    andExpr,
                    orExpr,
                    anyEvalExpr,
                    randomEvalExpr,
                    minEvalExpr,
                    maxEvalExpr,
                    uniqueEvalExpr
                    )

    addArithmExpr = arithmExpr << Token('+') << arithmExpr
    minusArithmExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multArithmExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerArithmExpr = arithmExpr << Token('**') << arithmExpr
    constantArithmExpr = Token('pi') | Token('e')

    parArithmExpr = '(' + arithmExpr + ')'

    unaryFuncArithmExpr = (T.cosf | T.sinf | T.tanf | T.expf | T.logf | T.absf | T.signf | T.floorf | T.ceilf | T.roundf
                           | T.acosf | T.asinf | T.atanf | T.shf | T.chf | T.thf | T.ashf | T.achf | T.athf | T.lenf
                           | T.rand | T.randint) \
                           + parArithmExpr
    binaryFuncArithmExpr = (T.minf | T.maxf) + '(' + arithmExpr + ',' + arithmExpr + ')'

    globalsKeyWord = T.globalsFpsKw | T.globalsHeightKw | T.globalsWidthKw
    globalsExpr = T.globalsKw + '(' + globalsKeyWord + ')'

    arithmExpr = Prio(T.integer, T.float, T.variable, T.string, constantArithmExpr,
                      globalsExpr, parArithmExpr,
                      unaryFuncArithmExpr, binaryFuncArithmExpr,
                      powerArithmExpr, multArithmExpr, minusArithmExpr, addArithmExpr)

    START = boolExpr
    COMMENTS = (                      # Allow C and Python comments
        Token(re="#(?:[^\r\n]*(?:\r\n?|\n\r?))") |
        Token(re="/[*](?:[^*]|[*][^/])*[*]/"))

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(TriggerParser, cls).parse(expr, tree_factory, on_error, log)
        return cls.buildExpression(tree)

    @classmethod
    def buildExpression(cls, tree):
        rootName = tree[0]

        def buildAnd():
            a1 = cls.buildExpression((tree[1]))
            a2 = cls.buildExpression((tree[3]))
            return And(a1, a2)

        def buildAnyEval():
            expr = cls.buildExpression(tree[2])
            return AnyEval(expr)

        def buildArithmetic():
            return cls.buildArithmeticExpression(tree)

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

        def buildDel():
            variable = cls.buildExpression(tree[2])
            return Del(variable)

        def buildDoubleNext():
            return cls.buildExpression(tree[2])

        def buildElock():
            priority = cls.buildExpression(tree[3])
            if len(tree) >= 6:
                args = cls.buildExpression(tree[5])
            else:
                args = []
            return eLock(priority, args)

        def buildELockParameters():
            return [cls.buildExpression(arg) for arg in tree[1::2]]

        def buildIs():
            variable = cls.buildExpression(tree[1])
            function = cls.buildExpression(tree[3])
            return Is(variable, function)

        def buildLitteral():
            return BLitteral(tree[1][1] == 'true')

        def buildMaxEvalExpr():
            arithmExpr = cls.buildExpression(tree[3])
            expr = cls.buildExpression(tree[5])
            return SelectMaxEval(expr, arithmExpr)

        def buildMinEvalExpr():
            arithmExpr = cls.buildExpression(tree[3])
            expr = cls.buildExpression(tree[5])
            return SelectMinEval(expr, arithmExpr)

        def buildNamedParameter():
            name = cls.buildExpression(tree[1])
            parameter = cls.buildExpression(tree[3])
            return name, parameter

        def buildNext():
            return cls.buildExpression(tree[1])

        def buildNot():
            a1 = cls.buildExpression((tree[2]))
            return Not(a1)

        def buildOr():
            a1 = cls.buildExpression((tree[1]))
            a2 = cls.buildExpression((tree[3]))
            return Or(a1, a2)

        def buildParameterized():
            exprType, exprValue = cls.buildExpression(tree[1])

            exprTypeAction = {
                TriggerParser.T.prop: (PropertyTriggerExpression, 1),
                TriggerParser.T.event: (EventTriggerExpression, 1),
                TriggerParser.T.graphicsSprite: (SpriteTriggerExpression, 2),
                TriggerParser.T.graphicsLine: (LineTriggerExpression, 2),
                TriggerParser.T.graphicsOval: (OvalTriggerExpression, 2),
                TriggerParser.T.graphicsRect: (RectTriggerExpression, 2),
                TriggerParser.T.graphicsPolygon: (PolygonTriggerExpression, 2),
                TriggerParser.T.graphicsText: (TextTriggerExpression, 2)
            }

            clsCons, offset = exprTypeAction[exprType]
            args, kwargs = cls.buildExpression(tree[3])

            if offset > 0:
                name = exprValue[offset:]
                return clsCons(name, args, kwargs)
            else:
                return clsCons(args, kwargs)

        def buildParameterizedType():
            return tree[1][0], tree[1][1]

        def buildParameters():
            buildArgs = [cls.buildExpression(arg) for arg in tree[1::2]]
            args = [arg for arg in buildArgs if not isinstance(arg, tuple)]
            kwargs = {kwarg[0]: kwarg[1] for kwarg in buildArgs if isinstance(kwarg, tuple)}
            return args, kwargs

        def buildRandomEval():
            expr = cls.buildExpression(tree[2])
            return RandomEval(expr)

        def buildTimer():
            nbFrames = cls.buildExpression((tree[3]))
            return Timer(nbFrames)

        def buildUniqueEvalExpr():
            expr = cls.buildExpression(tree[2])
            return UniqueEval(expr)

        def keywordColorValue():
            return KEYWORD_COLOR

        def keywordFileNameValue():
            return KEYWORD_FILENAME

        def keywordFontNameValue():
            return KEYWORD_FONT_NAME

        def keywordFontSizeValue():
            return KEYWORD_FONT_SIZE

        def keywordHValue():
            return KEYWORD_H

        def keywordIdValue():
            return KEYWORD_ID

        def keywordRotateValue():
            return KEYWORD_ROTATE

        def keywordScaleValue():
            return KEYWORD_SCALE

        def keywordTextValue():
            return KEYWORD_TEXT

        def keywordWidthValue():
            return KEYWORD_WIDTH

        def keywordWValue():
            return KEYWORD_W

        def keywordXIntValue():
            value = int(tree[1][1:])
            return KEYWORD_X_INT[value]

        def keywordXValue():
            return KEYWORD_X

        def keywordYIntValue():
            value = int(tree[1][1:])
            return KEYWORD_Y_INT[value]

        def keywordYValue():
            return KEYWORD_Y

        def keywordZValue():
            return KEYWORD_Z

        def unnamedVariableValue():
            return UndefinedLitteral()

        def value():
            return tree[1]

        def variableValue():
            return Variable(tree[1])

        booleanSymbols = {
            TriggerParser.T.variable: variableValue,
            TriggerParser.T.uvariable: unnamedVariableValue,

            TriggerParser.T.idkw: keywordIdValue,

            TriggerParser.T.coordX: keywordXValue,
            TriggerParser.T.coordY: keywordYValue,
            TriggerParser.T.coordZ: keywordZValue,
            TriggerParser.T.coordXInt: keywordXIntValue,
            TriggerParser.T.coordYInt: keywordYIntValue,
            TriggerParser.T.coordW: keywordWValue,
            TriggerParser.T.coordH: keywordHValue,
            TriggerParser.T.rotate: keywordRotateValue,
            TriggerParser.T.scale: keywordScaleValue,

            TriggerParser.T.fileName: keywordFileNameValue,
            TriggerParser.T.color: keywordColorValue,
            TriggerParser.T.width: keywordWidthValue,
            TriggerParser.T.text: keywordTextValue,
            TriggerParser.T.fontName: keywordFontNameValue,
            TriggerParser.T.fontSize: keywordFontSizeValue,

            TriggerParser.arithmExpr: buildArithmetic,

            TriggerParser.boolExpr: buildNext,
            TriggerParser.litExpr: buildLitteral,
            TriggerParser.timerExpr: buildTimer,

            TriggerParser.eLockParameters: buildELockParameters,
            TriggerParser.eLockExpr: buildElock,

            TriggerParser.parameter: buildNext,
            TriggerParser.namedParameterKW: buildNext,
            TriggerParser.namedParameter: buildNamedParameter,
            TriggerParser.parameters: buildParameters,
            TriggerParser.parameterizedType: buildParameterizedType,

            TriggerParser.parameterizedExpr: buildParameterized,

            TriggerParser.compareArithmExpr: buildCompare,
            TriggerParser.andExpr: buildAnd,
            TriggerParser.orExpr: buildOr,
            TriggerParser.notExpr: buildNot,
            TriggerParser.isExpr: buildIs,
            TriggerParser.delExpr: buildDel,

            TriggerParser.parExpr: buildDoubleNext,

            TriggerParser.anyEvalExpr: buildAnyEval,
            TriggerParser.randomEvalExpr: buildRandomEval,
            TriggerParser.minEvalExpr: buildMinEvalExpr,
            TriggerParser.maxEvalExpr: buildMaxEvalExpr,
            TriggerParser.uniqueEvalExpr: buildUniqueEvalExpr,

            TriggerParser.parArithmExpr: buildArithmetic,

            TriggerParser.START: buildNext,

        }

        return booleanSymbols[rootName]()

    @classmethod
    def buildArithmeticExpression(cls, tree):
        rootName = tree[0]

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

        def buildBinaryFunctionExpression():
            x1 = cls.buildArithmeticExpression(tree[3])
            x2 = cls.buildArithmeticExpression(tree[5])
            if tree[1][1] == 'min':
                return Min(x1, x2)
            elif tree[1][1] == 'max':
                return Max(x1, x2)

        def buildConstant():
            from math import pi, e
            if tree[1][1] == 'pi':
                value = pi
            else:
                value = e
            return ALitteral(value)

        def buildGlobalFpsKeyWord():
            return globalsFpsExpression

        def buildGlobalWidthKeyWord():
            return globalsWidthExpression

        def buildGlobalHeightKeyWord():
            return globalsHeightExpression

        def buildMinusExpression():
            if len(tree) == 4:
                return buildBinaryExpression()
            else:
                a1 = cls.buildArithmeticExpression(tree[2])
                return Subtraction(ALitteral(0), a1)

        def buildNext(i):
            def _buildNext():
                return cls.buildArithmeticExpression(tree[i])
            return _buildNext

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
            elif tree[1][1] == 'round':
                return Func(a, round)
            elif tree[1][1] == 'len':
                return Func(a, len)
            elif tree[1][1] == 'rand':
                def _random(x):
                    return random() * x
                return Func(a, _random)
            elif tree[1][1] == 'randint':
                def _randint(x):
                    return randint(0, x - 1)
                return Func(a, _randint)

        def intvalue():
            return ALitteral(int(tree[1]))

        def floatvalue():
            return ALitteral(float(tree[1]))

        def stringWithoutQuotes():
            return ALitteral(tree[1][1:-1])

        def variableValue():
            return ALitteral(Variable(tree[1]))

        arithmeticSymbols = {
            TriggerParser.T.integer: intvalue,
            TriggerParser.T.float: floatvalue,
            TriggerParser.T.string: stringWithoutQuotes,
            TriggerParser.T.variable: variableValue,

            TriggerParser.T.globalsFpsKw: buildGlobalFpsKeyWord,
            TriggerParser.T.globalsHeightKw: buildGlobalHeightKeyWord,
            TriggerParser.T.globalsWidthKw: buildGlobalWidthKeyWord,

            TriggerParser.arithmExpr: buildNext(1),
            TriggerParser.addArithmExpr: buildBinaryExpression,
            TriggerParser.minusArithmExpr: buildMinusExpression,
            TriggerParser.multArithmExpr: buildBinaryExpression,
            TriggerParser.powerArithmExpr: buildBinaryExpression,
            TriggerParser.constantArithmExpr: buildConstant,
            TriggerParser.parArithmExpr: buildNext(2),
            TriggerParser.unaryFuncArithmExpr: buildUnaryFunctionExpression,
            TriggerParser.binaryFuncArithmExpr: buildBinaryFunctionExpression,
            TriggerParser.globalsKeyWord: buildNext(1),
            TriggerParser.globalsExpr: buildNext(3)
        }

        return arithmeticSymbols[rootName]()

if __name__ == '__main__':
    # print BooleanExpressionParser.pre_compile_grammar()

    # from database import Property
    # from triggerExpressions import BExpression
    #
    # Property.add('Test', [1, 2], {})
    # Property.add('Test', [1, 3], {})
    # Property.add('Test', [2, 4], {})
    # Property.add('Test', [1, 5], {})
    #
    # expr = 'pTest(X,Y)'
    # expr = BExpression(TriggerParser.parse(expr))
    # print expr
    # for evaluation in expr.eval(None):
    #     print evaluation
    #
    # print
    #
    # expr = 'anyEval(pTest(X,Y))'
    # expr = BExpression(TriggerParser.parse(expr))
    # print expr
    # for evaluation in expr.eval(None):
    #     print evaluation
    #
    # print
    #
    # expr = 'randomEval(pTest(X,Y))'
    # expr = BExpression(TriggerParser.parse(expr))
    # print expr
    # for evaluation in expr.eval(None):
    #     print evaluation
    #
    # print
    #
    # expr = 'minEval(pTest(X,Y) or Z is 3 and X is 2 or Z is 2 and X is 1)[X + Z]'
    # expr = BExpression(TriggerParser.parse(expr))
    # print expr
    # for evaluation in expr.eval(None):
    #     print evaluation
    #
    # print
    #
    # expr = 'maxEval(pTest(X,Y) or Z is 8 and X is 2 or Z is 2 and X is 1)[X + Y]'
    # expr = BExpression(TriggerParser.parse(expr))
    # print expr
    # for evaluation in expr.eval(None):
    #     print evaluation

    from database import Property
    from triggerExpressions import BExpression

    expr = '(A + B ** 2) != (A + B ** 2)'
    expr = BExpression(TriggerParser.parse(expr))
    print expr