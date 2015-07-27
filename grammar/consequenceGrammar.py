import lrparsing
from lrparsing import List, Prio, Ref, Token, Opt, Sequence
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, \
    Power, Func, UndefinedLitteral, SelfLitteral, Min, Max, globalsFpsExpression, globalsHeightExpression, \
    globalsWidthExpression
from database import Variable
from grammar.Keywords import KEYWORD_ID, KEYWORD_CODE, \
    KEYWORD_Y, KEYWORD_X, KEYWORD_X_INT, KEYWORD_Y_INT, \
    KEYWORD_W, KEYWORD_H, KEYWORD_WIDTH, KEYWORD_COLOR, KEYWORD_FONT_NAME, KEYWORD_FONT_SIZE, KEYWORD_TEXT
from consequenceExpressions import AddPropertyConsequence, RemovePropertyConsequence, EditPropertyConsequence, \
    AddEventConsequence, AddSpriteConsequence, EditSpriteConsequence, RemoveSpriteConsequence, \
    AddSoundConsequence, \
    AddTokenConsequence, EditTokenConsequence, RemoveTokenConsequence, RemoveAllTokenConsequence, \
    AddTextConsequence, EditTextConsequence, RemoveTextConsequence, \
    RemoveLineConsequence, EditLineConsequence, AddLineConsequence, \
    AddRectConsequence, EditRectConsequence, RemoveRectConsequence, \
    AddOvalConsequence, EditOvalConsequence, RemoveOvalConsequence, \
    AddPolygonConsequence, EditPolygonConsequence, RemovePolygonConsequence, \
    PrintConsequence, EditGlobalFps, EditGlobalHeight, EditGlobalWidth, ClearAll


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
        token = Token('token')
        add = Token('add')
        remove = Token('remove')
        clear = Token('clear')
        all = Token('all')
        edit = Token('edit')
        printToken = Token('print')
        shapePolygon = Token('shpP')

        coordX = Token('x')
        coordY = Token('y')
        coordXInt = Token(re='x[1-9][0-9]*')
        coordYInt = Token(re='y[1-9][0-9]*')
        coordH = Token('h')
        coordW = Token('w')
        coords = Token('coords')

        code = Token('code')
        color = Token('color')
        width = Token('width')

        text = Token('text')
        fontName = Token('fontName')
        fontSize = Token('fontSize')

        shapeWidthKw = Token('width1')
        shapeColorKw = Token('color1')

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

        lenf = Token('len')

        minf = Token('min')
        maxf = Token('max')

        globalsKw = Token('globals')
        globalsFpsKw = Token('fps')
        globalsHeightKw = Token('screenHeight')
        globalsWidthKw = Token('screenWidth')

        idkw = Token('id')

    consExpr = Ref('consExpr')
    arithmExpr = Ref('arithmExpr')

    namedParameterKW = arithmExpr | \
                       T.coordX | T.coordY | \
                       T.coordXInt | T.coordYInt | \
                       T.coordH | T.coordW | \
                       T.code | \
                       T.color | T.width | \
                       T.text | T.fontName | T.fontSize

    namedParameter = namedParameterKW + '=' + arithmExpr
    parameters = \
        Prio(List(arithmExpr, Token(',')) + Opt(',' + List(namedParameter, Token(','))),
             List(namedParameter, Token(',')))

    incompleteNamedParameter = namedParameterKW + '=' + (T.uvariable | arithmExpr)
    incompleteParameters = \
        Prio(List((arithmExpr, T.uvariable), Token(',')) + Opt(',' + List(incompleteNamedParameter, Token(','))),
             List(incompleteNamedParameter, Token(',')))

    clearAllExpr = T.clear + T.all

    addType = T.prop | T.event | \
              T.graphicsSprite | T.graphicsLine | T.graphicsOval | T.graphicsRect | T.graphicsPolygon | \
              T.graphicsText
    editType = T.prop | \
               T.graphicsSprite | T.graphicsLine | T.graphicsOval | T.graphicsRect | T.graphicsPolygon | \
               T.graphicsText
    removeType = T.prop | \
                 T.graphicsSprite | T.graphicsLine | T.graphicsOval | T.graphicsRect | T.graphicsPolygon | \
                 T.graphicsText

    addExpr = T.add + addType +\
              '(' + parameters + ')'
    removeExpr = T.remove + removeType + '(' + incompleteParameters + ')'
    editExpr = T.edit + editType + '(' + incompleteParameters + '|' + incompleteParameters + ')'

    addTokenExpr = T.add + T.token + '(' + arithmExpr + Opt(',' + parameters) + ')'
    editTokenExpr = T.edit + T.token + '(' + Opt(incompleteParameters) + ')'
    removeTokenExpr = T.remove + T.token
    removeAllTokenExpr = T.remove + T.all + T.token

    addSoundExpr = T.add + T.sound + '(' + arithmExpr + ')'

    printExpr = T.printToken + List(arithmExpr, Token(','))

    globalsKeyWord = T.globalsFpsKw | T.globalsHeightKw | T.globalsWidthKw
    editGlobalsExpr = T.edit + T.globalsKw + '(' + globalsKeyWord + ',' + arithmExpr + ')'

    consExpr = Prio(clearAllExpr,
                    addExpr, removeExpr, editExpr,
                    addSoundExpr,
                    addTokenExpr, editTokenExpr, removeTokenExpr, removeAllTokenExpr,
                    printExpr, editGlobalsExpr)

    # listExpr = '[' + List(arithmExpr, Token(',')) + ']'
    # linkedListExpr = 'll' + listExpr
    # setExpr = 'set' + listExpr

    addArithmExpr = arithmExpr << Token('+') << arithmExpr
    minusArithmExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multArithmExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerArithmExpr = arithmExpr << Token('**') << arithmExpr
    constantExpr = Token('pi') | Token('e')
    parArithmExpr = '(' + arithmExpr + ')'

    unaryFuncExpr = (T.cosf | T.sinf | T.tanf | T.expf | T.logf | T.absf | T.signf | T.floorf | T.ceilf | T.roundf
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

    globalsExpr = T.globalsKw + '(' + globalsKeyWord + ')'

    arithmExpr = Prio(T.integer, T.float, T.variable, T.selfvariable, T.string, constantExpr,
                      globalsExpr,
                      # listExpr,
                      # linkedListExpr,
                      # setExpr,
                      parArithmExpr,
                      # getItemExpr, getSublistExpr, insertExpr, removeExpr,
                      unaryFuncExpr, binaryFuncExpr, powerArithmExpr, multArithmExpr, minusArithmExpr, addArithmExpr)
    # arithmExpr = Prio(T.integer, T.float, T.variable, T.string, constantExpr, parArithmExpr,
    #                   funcExpr, powerArithExpr, multArithExpr, addArithExpr, minusArithExpr)

    START = consExpr

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(ConsequenceParser, cls).parse(expr, tree_factory, on_error, log)
        return cls.buildExpression(tree)

    @classmethod
    def buildExpression(cls, tree):
        rootName = tree[0]

        def buildNext():
            return cls.buildExpression(tree[1])

        def clearAll():
            return ClearAll()

        def buildMultiTypes():
            chosenType = tree[1]
            return chosenType[0], chosenType[1]

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

        def buildAddSound():
            num = cls.buildExpression(tree[4])
            return AddSoundConsequence(num)

        def buildAddToken():
            nodeNum = cls.buildExpression(tree[4])
            if len(tree) == 6:
                return AddTokenConsequence(nodeNum, [], {})
            else:
                args, kwargs = cls.buildExpression(tree[6])
                return AddTokenConsequence(nodeNum, args, kwargs)

        def buildEditToken():
            if len(tree) == 5:
                return EditTokenConsequence([], {})
            else:
                args, kwargs = cls.buildExpression(tree[4])
                return EditTokenConsequence(args, kwargs)

        def buildRemoveToken():
            return RemoveTokenConsequence()

        def buildRemoveAllToken():
            return RemoveAllTokenConsequence()

        def unnamedVariableValue():
            return UndefinedLitteral()

        def keywordIdValue():
            return KEYWORD_ID

        def keywordCodeValue():
            return KEYWORD_CODE

        def keywordXValue():
            return KEYWORD_X

        def keywordYValue():
            return KEYWORD_Y

        def keywordXIntValue():
            value = int(tree[1][1:])
            return KEYWORD_X_INT[value]

        def keywordYIntValue():
            value = int(tree[1][1:])
            return KEYWORD_Y_INT[value]

        def keywordHValue():
            return KEYWORD_H

        def keywordWValue():
            return KEYWORD_W

        def keywordColorValue():
            return KEYWORD_COLOR

        def keywordTextValue():
            return KEYWORD_TEXT

        def keywordFontNameValue():
            return KEYWORD_FONT_NAME

        def keywordFontSizeValue():
            return KEYWORD_FONT_SIZE

        def keywordWidthValue():
            return KEYWORD_WIDTH

        def buildNamedParameter():
            name = cls.buildExpression(tree[1])
            parameter = cls.buildExpression(tree[3])
            return name, parameter

        def buildParameters():
            buildArgs = [cls.buildExpression(arg) for arg in tree[1::2]]
            args = [arg for arg in buildArgs if not isinstance(arg, tuple)]
            kwargs = {kwarg[0]: kwarg[1] for kwarg in buildArgs if isinstance(kwarg, tuple)}
            return args, kwargs

        def buildArithmetic():
            return cls.buildArithmeticExpression(tree)

        def buildPrintExpr():
            toPrint = [cls.buildExpression(arg) for arg in tree[2::2]]
            return PrintConsequence(toPrint)

        def buildEditGlobals():
            keywordClass = cls.buildSpecialExpression(tree[4])
            newValue = cls.buildArithmeticExpression(tree[6])
            return keywordClass(newValue)

        exprSymbols = {
            ConsequenceParser.START: buildNext,
            ConsequenceParser.consExpr: buildNext,
            ConsequenceParser.clearAllExpr: clearAll,


            ConsequenceParser.addType: buildMultiTypes,
            ConsequenceParser.removeType: buildMultiTypes,
            ConsequenceParser.editType: buildMultiTypes,

            ConsequenceParser.T.uvariable: unnamedVariableValue,

            ConsequenceParser.T.idkw: keywordIdValue,
            ConsequenceParser.T.code: keywordCodeValue,
            ConsequenceParser.T.coordX: keywordXValue,
            ConsequenceParser.T.coordY: keywordYValue,
            ConsequenceParser.T.coordXInt: keywordXIntValue,
            ConsequenceParser.T.coordYInt: keywordYIntValue,
            ConsequenceParser.T.coordH: keywordHValue,
            ConsequenceParser.T.coordW: keywordWValue,
            ConsequenceParser.T.color: keywordColorValue,
            ConsequenceParser.T.width: keywordWidthValue,
            ConsequenceParser.T.text: keywordTextValue,
            ConsequenceParser.T.fontName: keywordFontNameValue,
            ConsequenceParser.T.fontSize: keywordFontSizeValue,

            ConsequenceParser.addExpr: buildAdd,
            ConsequenceParser.removeExpr: buildRemove,
            ConsequenceParser.editExpr: buildEdit,

            ConsequenceParser.namedParameterKW: buildNext,
            ConsequenceParser.namedParameter: buildNamedParameter,
            ConsequenceParser.parameters: buildParameters,
            ConsequenceParser.incompleteNamedParameter: buildNamedParameter,
            ConsequenceParser.incompleteParameters: buildParameters,
            ConsequenceParser.addSoundExpr: buildAddSound,
            ConsequenceParser.addTokenExpr: buildAddToken,
            ConsequenceParser.editTokenExpr: buildEditToken,
            ConsequenceParser.removeTokenExpr: buildRemoveToken,
            ConsequenceParser.removeAllTokenExpr: buildRemoveAllToken,
            ConsequenceParser.printExpr: buildPrintExpr,
            ConsequenceParser.editGlobalsExpr: buildEditGlobals,
            ConsequenceParser.arithmExpr: buildArithmetic
        }

        return exprSymbols[rootName]()

    @classmethod
    def buildArithmeticExpression(cls, tree):
        rootName = tree[0]

        def buildNext(i):
            def _buildNext():
                return cls.buildArithmeticExpression(tree[i])
            return _buildNext

        def stringWithoutQuotes():
            return ALitteral(tree[1][1:-1])

        def intvalue():
            return ALitteral(int(tree[1]))

        def floatvalue():
            return ALitteral(float(tree[1]))

        def variableValue():
            return ALitteral(Variable(tree[1]))

        def selfVariableValue():
            return SelfLitteral()

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

        def buildMinusExpression():
            if len(tree) == 4:
                return buildBinaryExpression()
            else:
                a1 = cls.buildArithmeticExpression(tree[2])
                return Subtraction(ALitteral(0), a1)

        def buildConstant():
            from math import pi, e
            if tree[1][1] == 'pi':
                value = pi
            else:
                value = e
            return ALitteral(value)

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
            elif tree[1][1] == 'round':
                return Func(a, round)

        def buildBinaryFunctionExpression():
            x1 = cls.buildArithmeticExpression(tree[3])
            x2 = cls.buildArithmeticExpression(tree[5])
            if tree[1][1] == 'min':
                return Min(x1, x2)
            elif tree[1][1] == 'max':
                return Max(x1, x2)

        def buildGlobalFpsKeyWord():
            return globalsFpsExpression

        def buildGlobalWidthKeyWord():
            return globalsWidthExpression

        def buildGlobalHeightKeyWord():
            return globalsHeightExpression

        arithmeticSymbols = {
            ConsequenceParser.arithmExpr: buildNext(1),
            ConsequenceParser.parArithmExpr: buildNext(2),
            ConsequenceParser.T.integer: intvalue,
            ConsequenceParser.T.float: floatvalue,
            ConsequenceParser.T.variable: variableValue,
            ConsequenceParser.T.selfvariable: selfVariableValue,
            ConsequenceParser.T.string: stringWithoutQuotes,
            # ConsequenceParser.listExpr: listValue,
            # ConsequenceParser.linkedListExpr: linkedListValue,
            # ConsequenceParser.setExpr: setValue,
            # ConsequenceParser.getItemArithExpr: buildGetItemExpression,
            # ConsequenceParser.getSublistArithExpr: buildGetSublistExpression,
            # ConsequenceParser.insertArithExpr: buildInsertExpression,
            # ConsequenceParser.removeArithExpr: buildRemoveExpression,
            ConsequenceParser.addArithmExpr: buildBinaryExpression,
            ConsequenceParser.minusArithmExpr: buildMinusExpression,
            ConsequenceParser.multArithmExpr: buildBinaryExpression,
            ConsequenceParser.powerArithmExpr: buildBinaryExpression,
            ConsequenceParser.constantExpr: buildConstant,
            ConsequenceParser.unaryFuncExpr: buildUnaryFunctionExpression,
            ConsequenceParser.binaryFuncExpr: buildBinaryFunctionExpression,
            ConsequenceParser.T.globalsFpsKw: buildGlobalFpsKeyWord,
            ConsequenceParser.T.globalsHeightKw: buildGlobalHeightKeyWord,
            ConsequenceParser.T.globalsWidthKw: buildGlobalWidthKeyWord,
            ConsequenceParser.globalsKeyWord: buildNext(1),
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
