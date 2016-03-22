import lrparsing
from lrparsing import List, Prio, Ref, Token, Opt
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, \
    Power, Func, UndefinedLitteral, SelfLitteral, Min, Max, globalsFpsExpression, globalsHeightExpression, \
    globalsWidthExpression
from database import Variable
from grammar.keywords import KEYWORD_ID, KEYWORD_FILENAME, \
    KEYWORD_Y, KEYWORD_X, KEYWORD_X_INT, KEYWORD_Y_INT, \
    KEYWORD_W, KEYWORD_H, KEYWORD_ROTATE, KEYWORD_SCALE, \
    KEYWORD_WIDTH, KEYWORD_COLOR, KEYWORD_FONT_NAME, KEYWORD_FONT_SIZE, KEYWORD_TEXT, KEYWORD_Z
from consequenceExpressions import AddPropertyConsequence, RemovePropertyConsequence, EditPropertyConsequence, \
    AddEventConsequence, AddSpriteConsequence, EditSpriteConsequence, RemoveSpriteConsequence, \
    AddSoundConsequence, \
    AddTokenConsequence, RemoveTokenConsequence, RemoveAllTokenConsequence, \
    AddVariableConsequence, EditVariableConsequence, RemoveVariableConsequence, \
    AddTextConsequence, EditTextConsequence, RemoveTextConsequence, \
    RemoveLineConsequence, EditLineConsequence, AddLineConsequence, \
    AddRectConsequence, EditRectConsequence, RemoveRectConsequence, \
    AddOvalConsequence, EditOvalConsequence, RemoveOvalConsequence, \
    AddPolygonConsequence, EditPolygonConsequence, RemovePolygonConsequence, \
    PrintConsequence, EditGlobalFps, EditGlobalHeight, EditGlobalWidth, ClearAll
from random import random, randint
from utils.mathutils import sign


class ConsequenceParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='[0-9]+')
        float = Token(re='-?[0-9]+\.[0-9]+')
        string = Token(re='\'[^\']*\'')

        variable = Token(re='[A-Z][A-Z_0-9]*')
        uvariable = Token('_')
        selfvariable = Token('@')

        prop = Token(re='p[A-Z][A-Za-z_0-9]*')
        event = Token(re='e[A-Z][A-Za-z_0-9]*')
        graphicsSprite = Token(re='gs[A-Z][A-Za-z_0-9]*')
        graphicsLine = Token(re='gl[A-Z][A-Za-z_0-9]*')
        graphicsOval = Token(re='go[A-Z][A-Za-z_0-9]*')
        graphicsRect = Token(re='gr[A-Z][A-Za-z_0-9]*')
        graphicsPolygon = Token(re='gp[A-Z][A-Za-z_0-9]*')
        graphicsText = Token(re='gt[A-Z][A-Za-z_0-9]*')
        sound = Token('sound')
        tokenName = Token(re='to[A-Z][A-Za-z_0-9]*')
        token = Token('token')

        all = Token('all')

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

        add = Token('add')
        remove = Token('remove')
        clear = Token('clear')
        edit = Token('edit')
        printToken = Token('print')

    consExpr = Ref('consExpr')
    arithmExpr = Ref('arithmExpr')

    namedParameterKW = arithmExpr | \
                       T.coordX | T.coordY | T.coordZ | \
                       T.coordXInt | T.coordYInt | \
                       T.coordH | T.coordW | \
                       T.rotate | T.scale | \
                       T.fileName | \
                       T.color | T.width | \
                       T.text | T.fontName | T.fontSize

    namedParameter = namedParameterKW + '=' + arithmExpr
    parameters = \
        Prio(List(arithmExpr, Token(',')) + Opt(',' + List(namedParameter, Token(','))),
             List(namedParameter, Token(',')))

    incompleteNamedParameter = namedParameterKW + '=' + (T.uvariable | arithmExpr)
    incompleteParameters = \
        Prio(List(Prio(arithmExpr, T.uvariable), Token(',')) + Opt(',' + List(incompleteNamedParameter, Token(','))),
             List(incompleteNamedParameter, Token(',')))
    idNamedParameter = T.idkw + '=' + arithmExpr

    addType = T.prop | T.event | \
              T.graphicsSprite | T.graphicsLine | T.graphicsOval | T.graphicsRect | T.graphicsPolygon | \
              T.graphicsText
    removeType = T.prop | \
                 T.graphicsSprite | T.graphicsLine | T.graphicsOval | T.graphicsRect | T.graphicsPolygon | \
                 T.graphicsText
    editType = T.prop | \
               T.graphicsSprite | T.graphicsLine | T.graphicsOval | T.graphicsRect | T.graphicsPolygon | \
               T.graphicsText

    addExpr = T.add + addType +\
              '(' + parameters + ')'
    removeExpr = T.remove + removeType + '(' + (incompleteParameters | idNamedParameter) + ')'
    editExpr = T.edit + editType + '(' + (incompleteParameters | idNamedParameter) + '|' + incompleteParameters + ')'

    asVariableExpr = T.variable + '=' + arithmExpr

    addTokenExpr = T.add + T.tokenName + '(' + Opt(List(Prio(T.variable, asVariableExpr), Token(','))) + ')'
    removeTokenExpr = T.remove + T.token
    removeAllTokenExpr = T.remove + T.all + T.token

    addSoundExpr = T.add + T.sound + '(' + arithmExpr + ')'

    addVariableExpr = T.add + T.variable
    editVariableExpr = T.edit + T.variable + arithmExpr
    removeVariableExpr = T.remove + T.variable

    printExpr = T.printToken + List(arithmExpr, Token(','))

    globalsKeyWord = T.globalsFpsKw | T.globalsHeightKw | T.globalsWidthKw
    editGlobalsExpr = T.edit + T.globalsKw + '(' + globalsKeyWord + ',' + arithmExpr + ')'

    clearAllExpr = T.clear + T.all

    consExpr = Prio(addExpr, removeExpr, editExpr,
                    addTokenExpr, removeTokenExpr, removeAllTokenExpr,
                    addVariableExpr, editVariableExpr, removeVariableExpr,
                    addSoundExpr, printExpr, editGlobalsExpr, clearAllExpr)

    addArithmExpr = arithmExpr << Token('+') << arithmExpr
    minusArithmExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multArithmExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerArithmExpr = arithmExpr << Token('**') << arithmExpr
    constantExpr = Token('pi') | Token('e')

    parArithmExpr = '(' + arithmExpr + ')'

    unaryFuncExpr = (T.cosf | T.sinf | T.tanf | T.expf | T.logf | T.absf | T.signf | T.floorf | T.ceilf | T.roundf
                           | T.acosf | T.asinf | T.atanf | T.shf | T.chf | T.thf | T.ashf | T.achf | T.athf | T.lenf
                           | T.rand | T.randint) \
                     + parArithmExpr
    binaryFuncExpr = (T.minf | T.maxf) + '(' + arithmExpr + ',' + arithmExpr + ')'

    globalsExpr = T.globalsKw + '(' + globalsKeyWord + ')'

    arithmExpr = Prio(T.integer, T.float, T.variable, T.selfvariable, T.string, constantExpr,
                      globalsExpr, parArithmExpr,
                      unaryFuncExpr, binaryFuncExpr,
                      powerArithmExpr, multArithmExpr, minusArithmExpr, addArithmExpr)

    START = consExpr
    COMMENTS = (                      # Allow C and Python comments
        Token(re="#(?:[^\r\n]*(?:\r\n?|\n\r?))") |
        Token(re="/[*](?:[^*]|[*][^/])*[*]/"))

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(ConsequenceParser, cls).parse(expr, tree_factory, on_error, log)
        return cls.buildExpression(tree)

    @classmethod
    def buildExpression(cls, tree):
        rootName = tree[0]

        def buildAdd():
            exprType, exprValue = cls.buildExpression(tree[2])

            exprTypeAction = {
                ConsequenceParser.T.prop: (AddPropertyConsequence, 1),
                ConsequenceParser.T.event: (AddEventConsequence, 1),
                ConsequenceParser.T.graphicsSprite: (AddSpriteConsequence, 2),
                ConsequenceParser.T.graphicsLine: (AddLineConsequence, 2),
                ConsequenceParser.T.graphicsOval: (AddOvalConsequence, 2),
                ConsequenceParser.T.graphicsRect: (AddRectConsequence, 2),
                ConsequenceParser.T.graphicsPolygon: (AddPolygonConsequence, 2),
                ConsequenceParser.T.graphicsText: (AddTextConsequence, 2)
            }

            clsCons, offset = exprTypeAction[exprType]
            name = exprValue[offset:]
            args, kwargs = cls.buildExpression(tree[4])
            return clsCons(name, args, kwargs)

        def buildAddSound():
            filename = cls.buildExpression(tree[4])
            return AddSoundConsequence(filename)

        def buildAddToken():
            nodeLabel = tree[2][1][2:]
            print len(tree), tree
            if len(tree) == 5:
                return AddTokenConsequence(nodeLabel, [])
            else:
                inputEvaluation = [cls.buildExpression(variable) for variable in tree[4::2]]
                return AddTokenConsequence(nodeLabel, inputEvaluation)

        def buildAddVariable():
            variable = cls.buildExpression(tree[2])
            return AddVariableConsequence(variable)

        def buildArithmetic():
            return cls.buildArithmeticExpression(tree)

        def buildAsVariable():
            variable = cls.buildExpression(tree[1])
            expr = cls.buildExpression(tree[3])
            return variable, expr

        def buildEdit():
            exprType, exprValue = cls.buildExpression(tree[2])

            exprTypeActions = {
                ConsequenceParser.T.prop: (EditPropertyConsequence, 1),
                ConsequenceParser.T.graphicsSprite: (EditSpriteConsequence, 2),
                ConsequenceParser.T.graphicsLine: (EditLineConsequence, 2),
                ConsequenceParser.T.graphicsOval: (EditOvalConsequence, 2),
                ConsequenceParser.T.graphicsRect: (EditRectConsequence, 2),
                ConsequenceParser.T.graphicsPolygon: (EditPolygonConsequence, 2),
                ConsequenceParser.T.graphicsText: (EditTextConsequence, 2)
            }

            clsCons, offset = exprTypeActions[exprType]
            name = exprValue[offset:]
            args1, kwargs1 = cls.buildExpression(tree[4])
            args2, kwargs2 = cls.buildExpression(tree[6])
            return clsCons(name, args1, kwargs1, args2, kwargs2)

        def buildEditGlobals():
            keywordClass = cls.buildSpecialExpression(tree[4])
            newValue = cls.buildArithmeticExpression(tree[6])
            return keywordClass(newValue)

        def buildIdNamedParameter():
            keywordId = cls.buildExpression(tree[1])
            idValue = cls.buildExpression(tree[3])
            return [], {keywordId: idValue}

        def buildEditVariable():
            variable = cls.buildExpression(tree[2])
            expr = cls.buildExpression(tree[3])
            return EditVariableConsequence(variable, expr)

        def buildMultiTypes():
            chosenType = tree[1]
            return chosenType[0], chosenType[1]

        def buildNamedParameter():
            name = cls.buildExpression(tree[1])
            parameter = cls.buildExpression(tree[3])
            return name, parameter

        def buildNext():
            return cls.buildExpression(tree[1])

        def buildParameters():
            buildArgs = [cls.buildExpression(arg) for arg in tree[1::2]]
            args = [arg for arg in buildArgs if not isinstance(arg, tuple)]
            kwargs = {kwarg[0]: kwarg[1] for kwarg in buildArgs if isinstance(kwarg, tuple)}
            return args, kwargs

        def buildPrintExpr():
            toPrint = [cls.buildExpression(arg) for arg in tree[2::2]]
            return PrintConsequence(toPrint)

        def buildRemove():
            exprType, exprValue = cls.buildExpression(tree[2])

            exprTypeActions = {
                ConsequenceParser.T.prop: (RemovePropertyConsequence, 1),
                ConsequenceParser.T.graphicsSprite: (RemoveSpriteConsequence, 2),
                ConsequenceParser.T.graphicsLine: (RemoveLineConsequence, 2),
                ConsequenceParser.T.graphicsOval: (RemoveOvalConsequence, 2),
                ConsequenceParser.T.graphicsRect: (RemoveRectConsequence, 2),
                ConsequenceParser.T.graphicsPolygon: (RemovePolygonConsequence, 2),
                ConsequenceParser.T.graphicsText: (RemoveTextConsequence, 2)

            }

            clsCons, offset = exprTypeActions[exprType]
            name = exprValue[offset:]
            args, kwargs = cls.buildExpression(tree[4])
            return clsCons(name, args, kwargs)

        def buildRemoveAllToken():
            return RemoveAllTokenConsequence()

        def buildRemoveToken():
            return RemoveTokenConsequence()

        def buildRemoveVariable():
            variable = cls.buildExpression(tree[2])
            return RemoveVariableConsequence(variable)

        def clearAll():
            return ClearAll()

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

        def variableValue():
            return Variable(tree[1])

        exprSymbols = {

            ConsequenceParser.T.variable: variableValue,
            ConsequenceParser.T.uvariable: unnamedVariableValue,

            ConsequenceParser.T.idkw: keywordIdValue,

            ConsequenceParser.T.coordX: keywordXValue,
            ConsequenceParser.T.coordY: keywordYValue,
            ConsequenceParser.T.coordZ: keywordZValue,
            ConsequenceParser.T.coordXInt: keywordXIntValue,
            ConsequenceParser.T.coordYInt: keywordYIntValue,
            ConsequenceParser.T.coordW: keywordWValue,
            ConsequenceParser.T.coordH: keywordHValue,
            ConsequenceParser.T.rotate: keywordRotateValue,
            ConsequenceParser.T.scale: keywordScaleValue,

            ConsequenceParser.T.fileName: keywordFileNameValue,
            ConsequenceParser.T.color: keywordColorValue,
            ConsequenceParser.T.width: keywordWidthValue,
            ConsequenceParser.T.text: keywordTextValue,
            ConsequenceParser.T.fontName: keywordFontNameValue,
            ConsequenceParser.T.fontSize: keywordFontSizeValue,

            ConsequenceParser.consExpr: buildNext,

            ConsequenceParser.namedParameterKW: buildNext,
            ConsequenceParser.namedParameter: buildNamedParameter,
            ConsequenceParser.parameters: buildParameters,
            ConsequenceParser.incompleteNamedParameter: buildNamedParameter,
            ConsequenceParser.incompleteParameters: buildParameters,
            ConsequenceParser.idNamedParameter: buildIdNamedParameter,

            ConsequenceParser.addType: buildMultiTypes,
            ConsequenceParser.removeType: buildMultiTypes,
            ConsequenceParser.editType: buildMultiTypes,

            ConsequenceParser.addExpr: buildAdd,
            ConsequenceParser.removeExpr: buildRemove,
            ConsequenceParser.editExpr: buildEdit,

            ConsequenceParser.asVariableExpr: buildAsVariable,

            ConsequenceParser.addTokenExpr: buildAddToken,
            ConsequenceParser.removeTokenExpr: buildRemoveToken,
            ConsequenceParser.removeAllTokenExpr: buildRemoveAllToken,

            ConsequenceParser.addVariableExpr: buildAddVariable,
            ConsequenceParser.editVariableExpr: buildEditVariable,
            ConsequenceParser.removeVariableExpr: buildRemoveVariable,

            ConsequenceParser.addSoundExpr: buildAddSound,
            ConsequenceParser.printExpr: buildPrintExpr,
            ConsequenceParser.editGlobalsExpr: buildEditGlobals,
            ConsequenceParser.clearAllExpr: clearAll,

            ConsequenceParser.arithmExpr: buildArithmetic,

            ConsequenceParser.START: buildNext,
        }

        return exprSymbols[rootName]()

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

        def buildGlobalHeightKeyWord():
            return globalsHeightExpression

        def buildGlobalWidthKeyWord():
            return globalsWidthExpression

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
                return Func(a, sign)
            elif tree[1][1] == 'ceil':
                from math import ceil
                return Func(a, ceil)
            elif tree[1][1] == 'floor':
                from math import floor
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

        def floatvalue():
            return ALitteral(float(tree[1]))

        def intvalue():
            return ALitteral(int(tree[1]))

        def selfVariableValue():
            return SelfLitteral()

        def stringWithoutQuotes():
            return ALitteral(tree[1][1:-1])

        def variableValue():
            return ALitteral(Variable(tree[1]))

        arithmeticSymbols = {
            ConsequenceParser.T.integer: intvalue,
            ConsequenceParser.T.float: floatvalue,
            ConsequenceParser.T.string: stringWithoutQuotes,

            ConsequenceParser.T.variable: variableValue,
            ConsequenceParser.T.selfvariable: selfVariableValue,

            ConsequenceParser.T.globalsFpsKw: buildGlobalFpsKeyWord,
            ConsequenceParser.T.globalsHeightKw: buildGlobalHeightKeyWord,
            ConsequenceParser.T.globalsWidthKw: buildGlobalWidthKeyWord,

            ConsequenceParser.globalsKeyWord: buildNext(1),

            ConsequenceParser.arithmExpr: buildNext(1),

            ConsequenceParser.addArithmExpr: buildBinaryExpression,
            ConsequenceParser.minusArithmExpr: buildMinusExpression,
            ConsequenceParser.multArithmExpr: buildBinaryExpression,
            ConsequenceParser.powerArithmExpr: buildBinaryExpression,
            ConsequenceParser.constantExpr: buildConstant,

            ConsequenceParser.parArithmExpr: buildNext(2),

            ConsequenceParser.unaryFuncExpr: buildUnaryFunctionExpression,
            ConsequenceParser.binaryFuncExpr: buildBinaryFunctionExpression,

            ConsequenceParser.globalsExpr: buildNext(3)
        }

        return arithmeticSymbols[rootName]()

    @classmethod
    def buildSpecialExpression(cls, tree):
        rootName = tree[0]

        def buildNext():
            return cls.buildSpecialExpression(tree[1])

        def buildGlobalFpsKeyWord():
            return EditGlobalFps

        def buildGlobalHeightKeyWord():
            return EditGlobalHeight

        def buildGlobalWidthKeyWord():
            return EditGlobalWidth

        specialSymbols = {
            ConsequenceParser.globalsKeyWord: buildNext,
            ConsequenceParser.T.globalsFpsKw: buildGlobalFpsKeyWord,
            ConsequenceParser.T.globalsHeightKw: buildGlobalHeightKeyWord,
            ConsequenceParser.T.globalsWidthKw: buildGlobalWidthKeyWord
        }

        return specialSymbols[rootName]()

if __name__ == '__main__':
    print ConsequenceParser.pre_compile_grammar()
    expr = 'print min(3,5+3)'
    print ConsequenceParser.parse(expr)
