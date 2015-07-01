import lrparsing
from lrparsing import List, Prio, Ref, Token, Opt, Sequence
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, \
    Power, Func, UndefinedLitteral, SelfLitteral, Min, Max, globalsFpsExpression, globalsHeightExpression, \
    globalsWidthExpression
from database import Variable, KEYWORD_ID
from consequenceExpressions import AddPropertyConsequence, RemovePropertyConsequence, EditPropertyConsequence, \
    AddEventConsequence, AddSpriteConsequence, EditSpriteConsequence, RemoveSpriteConsequence, \
    AddTokenConsequence, EditTokenConsequence, RemoveTokenConsequence, AddTextConsequence, EditTextConsequence, \
    RemoveTextConsequence, RemoveLineConsequence, EditLineConsequence, AddLineConsequence, AddRectConsequence, \
    EditRectConsequence, RemoveRectConsequence, AddOvalConsequence, EditOvalConsequence, \
    RemoveOvalConsequence, AddPolygonConsequence, EditPolygonConsequence, RemovePolygonConsequence, PrintConsequence


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
        sprite = Token('s')
        text = Token('t')
        token = Token('token')
        add = Token('add')
        remove = Token('remove')
        move = Token('move')
        edit = Token('edit')
        printToken = Token('print')
        shapeLine = Token('shpL')
        shapeRect = Token('shpR')
        shapeOval = Token('shpO')
        shapePolygon = Token('shpP')

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

        globalsKw = Token('globals')
        globalsFpsKw = Token('fps')
        globalsHeightKw = Token('height')
        globalsWidthKw = Token('width')

        idkw = Token('id')

    consExpr = Ref('consExpr')
    arithmExpr = Ref('arithmExpr')

    namedParameter = arithmExpr + '=' + arithmExpr
    parameters = \
        Prio(List(arithmExpr, Token(',')) + Opt(',' + List(namedParameter, Token(','))),
             List(namedParameter, Token(',')))
    incompleteNamedParameter = (arithmExpr | T.idkw) + Token('=') + (arithmExpr, T.uvariable)
    incompleteParameters = \
        Prio(List((arithmExpr, T.uvariable), Token(',')) + Opt(',' + List(incompleteNamedParameter, Token(','))),
             List(incompleteNamedParameter, Token(',')))

    addPropExpr = T.add + T.prop + '(' + parameters + ')'
    removePropExpr = T.remove + T.prop + '(' + incompleteParameters + ')'
    editPropExpr = T.edit + T.prop + '(' + incompleteParameters + '|' + incompleteParameters + ')'
    addEventExpr = T.add + T.event + '(' + parameters + ')'

    addTokenExpr = T.add + T.token + '(' + arithmExpr + Opt(',' + parameters) + ')'
    editTokenExpr = T.edit + T.token + '(' + Opt(incompleteParameters) + ')'
    removeTokenExpr = T.remove + T.token

    addSpriteExpr = T.add + T.sprite + '(' + arithmExpr + ',' + arithmExpr + ',' + \
                    arithmExpr + ',' + arithmExpr + ')'
    editSpriteExpr = T.edit + T.sprite + '(' + arithmExpr + ',' + (arithmExpr, T.uvariable) + ',' + \
                    (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ')'
    removeSpriteExpr = T.remove + T.sprite + '(' + arithmExpr + ')'

    addTextExpr = T.add + T.text + '(' + arithmExpr + ',' + arithmExpr + ',' + \
                  arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ')'
    editTextExpr = T.edit + T.text + '(' + arithmExpr + ',' + (arithmExpr, T.uvariable) + ',' + \
                   (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' + \
                   (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ')'
    removeTextExpr = T.remove + T.text + '(' + arithmExpr + ')'

    addLineExpr = T.add + T.shapeLine + '(' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + \
                  arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ')'
    editLineExpr = T.edit + T.shapeLine + '(' + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' \
                   + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ','\
                   + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' \
                   + (arithmExpr, T.uvariable) + ')'
    removeLineExpr = T.remove + T.shapeLine + '(' + arithmExpr + ')'

    addRectExpr = T.add + T.shapeRect + '(' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + \
                  arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ')'
    editRectExpr = T.edit + T.shapeRect + '(' + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' \
                   + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ','\
                   + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' \
                   + (arithmExpr, T.uvariable) + ')'
    removeRectExpr = T.remove + T.shapeRect + '(' + arithmExpr + ')'

    addOvalExpr = T.add + T.shapeOval + '(' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + \
                  arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ',' + arithmExpr + ')'
    editOvalExpr = T.edit + T.shapeOval + '(' + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' \
                   + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ','\
                   + (arithmExpr, T.uvariable) + ',' + (arithmExpr, T.uvariable) + ',' \
                   + (arithmExpr, T.uvariable) + ')'
    removeOvalExpr = T.remove + T.shapeOval + '(' + arithmExpr + ')'

    listPoint = List('(' + arithmExpr + ',' + arithmExpr + ')', Token(','), min=2)
    addPolygonExpr = T.add + T.shapePolygon + '(' + arithmExpr + ',' + '[' + listPoint + ']' + ',' \
                     + arithmExpr + ',' + arithmExpr + ')'

    listEditPoint = List(Sequence('(', (arithmExpr, T.uvariable)) + ',' + (arithmExpr, T.uvariable) + ')', Token(','),
                         min=2)
    editPolygonExpr = T.edit + T.shapePolygon + '(' + (arithmExpr, T.uvariable) + ',' + '[' + listEditPoint + ']' + ',' \
                   + (arithmExpr, T.uvariable) + ',' \
                   + (arithmExpr, T.uvariable) + ')'
    removePolygonExpr = T.remove + T.shapePolygon + '(' + arithmExpr + ')'

    printExpr = T.printToken + List(arithmExpr, Token(','))

    consExpr = Prio(addPropExpr, removePropExpr, editPropExpr, addEventExpr, addSpriteExpr, removeSpriteExpr,
                    editSpriteExpr, addTextExpr, removeTextExpr, editTextExpr, addLineExpr, editLineExpr,
                    removeLineExpr, addRectExpr, editRectExpr, removeRectExpr, addOvalExpr, editOvalExpr,
                    removeOvalExpr, addPolygonExpr, editPolygonExpr, removePolygonExpr, addTokenExpr,
                    editTokenExpr, removeTokenExpr, printExpr)

    # listExpr = '[' + List(arithmExpr, Token(',')) + ']'
    # linkedListExpr = 'll' + listExpr
    # setExpr = 'set' + listExpr

    addArithmExpr = arithmExpr << Token('+') << arithmExpr
    minusArithmExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multArithmExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerArithmExpr = arithmExpr << Token('**') << arithmExpr
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

    globalsKeyWord = T.globalsFpsKw | T.globalsHeightKw | T.globalsWidthKw
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

        def buildAddProperty():
            name = cls.buildExpression(tree[2])[1:]
            args, kwargs = cls.buildExpression(tree[4])
            return AddPropertyConsequence(name, args, kwargs)

        def buildRemoveProperty():
            name = cls.buildExpression(tree[2])[1:]
            args, kwargs = cls.buildExpression(tree[4])
            return RemovePropertyConsequence(name, args, kwargs)

        def buildEditProperty():
            name = cls.buildExpression(tree[2])[1:]
            args1, kwargs1 = cls.buildExpression(tree[4])
            args2, kwargs2 = cls.buildExpression(tree[6])
            return EditPropertyConsequence(name, args1, kwargs1, args2, kwargs2)

        def buildAddEvent():
            name = cls.buildExpression(tree[2])[1:]
            args, kwargs = cls.buildExpression(tree[4])
            return AddEventConsequence(name, args, kwargs)

        def buildAddSprite():
            name = cls.buildExpression(tree[4])
            num = cls.buildExpression(tree[6])
            x = cls.buildExpression(tree[8])
            y = cls.buildExpression(tree[10])
            return AddSpriteConsequence(name, num, x, y)

        def buildEditSprite():
            name = cls.buildExpression(tree[4])
            num = cls.buildExpression(tree[6])
            x = cls.buildExpression(tree[8])
            y = cls.buildExpression(tree[10])
            return EditSpriteConsequence(name, num, x, y)

        def buildRemoveSprite():
            name = cls.buildExpression(tree[4])
            return RemoveSpriteConsequence(name)

        def buildAddText():
            name = cls.buildExpression(tree[4])
            text = cls.buildExpression(tree[6])
            x = cls.buildExpression(tree[8])
            y = cls.buildExpression(tree[10])
            color = cls.buildExpression(tree[12])
            font = cls.buildExpression(tree[14])
            fontSize = cls.buildExpression(tree[16])
            return AddTextConsequence(name, text, x, y, color, font, fontSize)

        def buildEditText():
            name = cls.buildExpression(tree[4])
            text = cls.buildExpression(tree[6])
            x = cls.buildExpression(tree[8])
            y = cls.buildExpression(tree[10])
            color = cls.buildExpression(tree[12])
            font = cls.buildExpression(tree[14])
            fontSize = cls.buildExpression(tree[16])
            return EditTextConsequence(name, text, x, y, color, font, fontSize)

        def buildRemoveText():
            name = cls.buildExpression(tree[4])
            return RemoveTextConsequence(name)

        def buildAddLine():
            name = cls.buildExpression(tree[4])
            x1 = cls.buildExpression(tree[6])
            y1 = cls.buildExpression(tree[8])
            x2 = cls.buildExpression(tree[10])
            y2 = cls.buildExpression(tree[12])
            width = cls.buildExpression(tree[14])
            colorName = cls.buildExpression(tree[16])
            return AddLineConsequence(name, x1, y1, x2, y2, width, colorName)

        def buildEditLine():
            name = cls.buildExpression(tree[4])
            x1 = cls.buildExpression(tree[6])
            y1 = cls.buildExpression(tree[8])
            x2 = cls.buildExpression(tree[10])
            y2 = cls.buildExpression(tree[12])
            width = cls.buildExpression(tree[14])
            colorName = cls.buildExpression(tree[16])
            return EditLineConsequence(name, x1, y1, x2, y2, width, colorName)

        def buildRemoveLine():
            name = cls.buildExpression(tree[4])
            return RemoveLineConsequence(name)

        def buildAddRect():
            name = cls.buildExpression(tree[4])
            x = cls.buildExpression(tree[6])
            y = cls.buildExpression(tree[8])
            w = cls.buildExpression(tree[10])
            h = cls.buildExpression(tree[12])
            width = cls.buildExpression(tree[14])
            colorName = cls.buildExpression(tree[16])
            return AddRectConsequence(name, x, y, w, h, width, colorName)

        def buildEditRect():
            name = cls.buildExpression(tree[4])
            x = cls.buildExpression(tree[6])
            y = cls.buildExpression(tree[8])
            w = cls.buildExpression(tree[10])
            h = cls.buildExpression(tree[12])
            width = cls.buildExpression(tree[14])
            colorName = cls.buildExpression(tree[16])
            return EditRectConsequence(name, x, y, w, h, width, colorName)

        def buildRemoveRect():
            name = cls.buildExpression(tree[4])
            return RemoveRectConsequence(name)

        def buildAddOval():
            name = cls.buildExpression(tree[4])
            x = cls.buildExpression(tree[6])
            y = cls.buildExpression(tree[8])
            a = cls.buildExpression(tree[10])
            b = cls.buildExpression(tree[12])
            width = cls.buildExpression(tree[14])
            colorName = cls.buildExpression(tree[16])
            return AddOvalConsequence(name, x, y, a, b, width, colorName)

        def buildEditOval():
            name = cls.buildExpression(tree[4])
            x = cls.buildExpression(tree[6])
            y = cls.buildExpression(tree[8])
            a = cls.buildExpression(tree[10])
            b = cls.buildExpression(tree[12])
            width = cls.buildExpression(tree[14])
            colorName = cls.buildExpression(tree[16])
            return EditOvalConsequence(name, x, y, a, b, width, colorName)

        def buildRemoveOval():
            name = cls.buildExpression(tree[4])
            return RemoveOvalConsequence(name)

        def buildListPoint():
            argsX = [cls.buildExpression(arg) for arg in tree[2::6]]
            argsY = [cls.buildExpression(arg) for arg in tree[4::6]]
            return zip(argsX, argsY)

        def buildAddPolygon():
            name = cls.buildExpression(tree[4])
            listPoint = cls.buildExpression(tree[7])
            width = cls.buildExpression(tree[10])
            colorName = cls.buildExpression(tree[12])
            return AddPolygonConsequence(name, listPoint, width, colorName)

        def buildListEditPoint():
            argsX = [cls.buildExpression(arg) for arg in tree[2::6]]
            argsY = [cls.buildExpression(arg) for arg in tree[4::6]]
            return zip(argsX, argsY)

        def buildEditPolygon():
            name = cls.buildExpression(tree[4])
            listEditPoint = cls.buildExpression(tree[7])
            width = cls.buildExpression(tree[10])
            colorName = cls.buildExpression(tree[12])
            return EditPolygonConsequence(name, listEditPoint, width, colorName)

        def buildRemovePolygon():
            name = cls.buildExpression(tree[4])
            return RemovePolygonConsequence(name)

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

        def value():
            return tree[1]

        def unnamedVariableValue():
            return UndefinedLitteral()

        def keywordIdValue():
            return KEYWORD_ID

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

        exprSymbols = {
            ConsequenceParser.START: buildNext,
            ConsequenceParser.consExpr: buildNext,
            ConsequenceParser.addPropExpr: buildAddProperty,
            ConsequenceParser.removePropExpr: buildRemoveProperty,
            ConsequenceParser.editPropExpr: buildEditProperty,
            ConsequenceParser.addEventExpr: buildAddEvent,
            ConsequenceParser.T.event: value,
            ConsequenceParser.T.prop: value,
            ConsequenceParser.T.uvariable: unnamedVariableValue,
            ConsequenceParser.T.idkw: keywordIdValue,
            ConsequenceParser.namedParameter: buildNamedParameter,
            ConsequenceParser.parameters: buildParameters,
            ConsequenceParser.incompleteNamedParameter: buildNamedParameter,
            ConsequenceParser.incompleteParameters: buildParameters,
            ConsequenceParser.addSpriteExpr: buildAddSprite,
            ConsequenceParser.removeSpriteExpr: buildRemoveSprite,
            ConsequenceParser.editSpriteExpr: buildEditSprite,
            ConsequenceParser.addTextExpr: buildAddText,
            ConsequenceParser.removeTextExpr: buildRemoveText,
            ConsequenceParser.editTextExpr: buildEditText,
            ConsequenceParser.addLineExpr: buildAddLine,
            ConsequenceParser.removeLineExpr: buildRemoveLine,
            ConsequenceParser.editLineExpr: buildEditLine,
            ConsequenceParser.addRectExpr: buildAddRect,
            ConsequenceParser.removeRectExpr: buildRemoveRect,
            ConsequenceParser.editRectExpr: buildEditRect,
            ConsequenceParser.addOvalExpr: buildAddOval,
            ConsequenceParser.removeOvalExpr: buildRemoveOval,
            ConsequenceParser.editOvalExpr: buildEditOval,
            ConsequenceParser.listPoint: buildListPoint,
            ConsequenceParser.addPolygonExpr: buildAddPolygon,
            ConsequenceParser.removePolygonExpr: buildRemovePolygon,
            ConsequenceParser.listEditPoint: buildListEditPoint,
            ConsequenceParser.editPolygonExpr: buildEditPolygon,
            ConsequenceParser.addTokenExpr: buildAddToken,
            ConsequenceParser.editTokenExpr: buildEditToken,
            ConsequenceParser.removeTokenExpr: buildRemoveToken,
            ConsequenceParser.printExpr: buildPrintExpr,
            ConsequenceParser.arithmExpr: buildArithmetic
        }

        return exprSymbols[rootName]()

    @classmethod
    def buildArithmeticExpression(cls, tree):
        rootName = tree[0]

        def buildNext():
            return cls.buildArithmeticExpression(tree[1])

        def buildDoubleNext():
            return cls.buildArithmeticExpression(tree[2])

        def buildTripleNext():
            return cls.buildArithmeticExpression(tree[3])

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
            ConsequenceParser.arithmExpr: buildNext,
            ConsequenceParser.parArithmExpr: buildDoubleNext,
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
            ConsequenceParser.globalsKeyWord: buildNext,
            ConsequenceParser.globalsExpr: buildTripleNext
        }

        return arithmeticSymbols[rootName]()


if __name__ == '__main__':
    print ConsequenceParser.pre_compile_grammar()
    expr = 'print min(3,5+3)'
    print ConsequenceParser.parse(expr)
