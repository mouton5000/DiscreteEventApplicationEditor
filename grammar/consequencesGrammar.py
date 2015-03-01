import lrparsing
from lrparsing import List, Prio, Ref, Token, Opt, Sequence
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, \
    Power, Func, ListLitteral, LinkedListLitteral, SetLitteral, GetItemExpression, GetSublistExpression, \
    InsertExpression, RemoveAllExpression, RemoveExpression, UndefinnedLitteral, SelfExpression, Min, Max
from database import Variable
from consequencesExpressions import AddPropertyConsequence, RemovePropertyConsequence, EditPropertyConsequence, \
    AddEventConsequence, AddSpriteConsequence, EditSpriteConsequence, RemoveSpriteConsequence, \
    AddTokenConsequence, EditTokenConsequence, RemoveTokenConsequence, AddTextConsequence, EditTextConsequence, \
    RemoveTextConsequence, RemoveLineConsequence, EditLineConsequence, AddLineConsequence, AddRectConsequence, \
    EditRectConsequence, RemoveRectConsequence, AddOvalConsequence, EditOvalConsequence, \
    RemoveOvalConsequence, AddPolygonConsequence, EditPolygonConsequence, RemovePolygonConsequence, PrintConsequence


class ConsequencesParser(lrparsing.Grammar):
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

    consExpr = Ref('consExpr')
    arithmExpr = Ref('arithmExpr')

    parameters = List(arithmExpr, Token(','))
    incompleteParameters = List((arithmExpr, T.uvariable), Token(','))

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

    printExpr = T.printToken + parameters

    consExpr = Prio(addPropExpr, removePropExpr, editPropExpr, addEventExpr, addSpriteExpr, removeSpriteExpr,
                    editSpriteExpr, addTextExpr, removeTextExpr, editTextExpr, addLineExpr, editLineExpr,
                    removeLineExpr, addRectExpr, editRectExpr, removeRectExpr, addOvalExpr, editOvalExpr,
                    removeOvalExpr, addPolygonExpr, editPolygonExpr, removePolygonExpr, addTokenExpr,
                    editTokenExpr, removeTokenExpr, printExpr)

    listExpr = '[' + List(arithmExpr, Token(',')) + ']'
    linkedListExpr = 'll' + listExpr
    setExpr = 'set' + listExpr

    addArithExpr = arithmExpr << Token('+') << arithmExpr
    minusArithExpr = Opt(arithmExpr) << Token('-') << arithmExpr
    multArithExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerArithExpr = arithmExpr << Token('**') << arithmExpr
    constantExpr = Token('pi') | Token('e')
    parArithmExpr = '(' + arithmExpr + ')'
    funcExpr = (Token('cos') | Token('sin') | Token('tan') | Token('exp') | Token('log') | Token('abs') |
                Token('sign') | Token('floor') | Token('ceil') | Token('acos') | Token('asin') | Token('atan') |
                Token('sh') | Token('ch') | Token('th') | Token('ash') | Token('ach') | Token('ath') | Token('len')) \
               + parArithmExpr
    minExpr = Token('min') + '(' + arithmExpr + ',' + arithmExpr + ')'
    maxExpr = Token('max') + '(' + arithmExpr + ',' + arithmExpr + ')'
    getItemArithExpr = arithmExpr + '[' + arithmExpr + ']'
    getSublistArithExpr = arithmExpr + '[' + Opt(arithmExpr) + ':' + Opt(arithmExpr) + ']'
    insertArithExpr = arithmExpr << '<' << Opt(arithmExpr) << '<' << arithmExpr
    removeArithExpr = arithmExpr << '>' << ((arithmExpr << '>') | ('>' << Opt('>') << arithmExpr))

    arithmExpr = Prio(T.integer, T.float, T.variable, T.selfvariable, T.string, constantExpr, listExpr, linkedListExpr,
                      setExpr, parArithmExpr, getItemArithExpr, getSublistArithExpr, insertArithExpr, removeArithExpr,
                      minExpr, maxExpr, funcExpr, powerArithExpr, multArithExpr, minusArithExpr, addArithExpr)

    # arithmExpr = Prio(T.integer, T.float, T.variable, T.string, constantExpr, parArithmExpr,
    #                   funcExpr, powerArithExpr, multArithExpr, addArithExpr, minusArithExpr)

    START = consExpr

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(ConsequencesParser, cls).parse(expr, tree_factory, on_error, log)
        return cls.buildExpression(tree)

    @classmethod
    def buildExpression(cls, tree):
        rootName = tree[0]

        def buildNext():
            return cls.buildExpression(tree[1])

        def buildAddProperty():
            name = cls.buildExpression(tree[2])[1:]
            args = cls.buildExpression(tree[4])
            return AddPropertyConsequence(name, args)

        def buildRemoveProperty():
            name = cls.buildExpression(tree[2])[1:]
            args = cls.buildExpression(tree[4])
            return RemovePropertyConsequence(name, args)

        def buildEditProperty():
            name = cls.buildExpression(tree[2])[1:]
            args1 = cls.buildExpression(tree[4])
            args2 = cls.buildExpression(tree[6])
            return EditPropertyConsequence(name, args1, args2)

        def buildAddEvent():
            name = cls.buildExpression(tree[2])[1:]
            args = cls.buildExpression(tree[4])
            return AddEventConsequence(name, args)

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
                return AddTokenConsequence(nodeNum, [])
            else:
                args = cls.buildExpression(tree[6])
                return AddTokenConsequence(nodeNum, args)

        def buildEditToken():
            if len(tree) == 5:
                return EditTokenConsequence([])
            else:
                args = cls.buildExpression(tree[4])
                return EditTokenConsequence(args)

        def buildRemoveToken():
            return RemoveTokenConsequence()

        def value():
            return tree[1]

        def unnamedVariableValue():
            return UndefinnedLitteral()

        def buildParameters():
            return [cls.buildExpression(arg) for arg in tree[1::2]]

        def buildArithmetic():
            return cls.buildArithmeticExpression(tree)

        def buildPrintExpr():
            toPrint = cls.buildExpression(tree[2])
            return PrintConsequence(toPrint)

        exprSymbols = {
            ConsequencesParser.START: buildNext,
            ConsequencesParser.consExpr: buildNext,
            ConsequencesParser.addPropExpr: buildAddProperty,
            ConsequencesParser.removePropExpr: buildRemoveProperty,
            ConsequencesParser.editPropExpr: buildEditProperty,
            ConsequencesParser.addEventExpr: buildAddEvent,
            ConsequencesParser.T.event: value,
            ConsequencesParser.T.prop: value,
            ConsequencesParser.T.uvariable: unnamedVariableValue,
            ConsequencesParser.parameters: buildParameters,
            ConsequencesParser.incompleteParameters: buildParameters,
            ConsequencesParser.addSpriteExpr: buildAddSprite,
            ConsequencesParser.removeSpriteExpr: buildRemoveSprite,
            ConsequencesParser.editSpriteExpr: buildEditSprite,
            ConsequencesParser.addTextExpr: buildAddText,
            ConsequencesParser.removeTextExpr: buildRemoveText,
            ConsequencesParser.editTextExpr: buildEditText,
            ConsequencesParser.addLineExpr: buildAddLine,
            ConsequencesParser.removeLineExpr: buildRemoveLine,
            ConsequencesParser.editLineExpr: buildEditLine,
            ConsequencesParser.addRectExpr: buildAddRect,
            ConsequencesParser.removeRectExpr: buildRemoveRect,
            ConsequencesParser.editRectExpr: buildEditRect,
            ConsequencesParser.addOvalExpr: buildAddOval,
            ConsequencesParser.removeOvalExpr: buildRemoveOval,
            ConsequencesParser.editOvalExpr: buildEditOval,
            ConsequencesParser.listPoint: buildListPoint,
            ConsequencesParser.addPolygonExpr: buildAddPolygon,
            ConsequencesParser.removePolygonExpr: buildRemovePolygon,
            ConsequencesParser.listEditPoint: buildListEditPoint,
            ConsequencesParser.editPolygonExpr: buildEditPolygon,
            ConsequencesParser.addTokenExpr: buildAddToken,
            ConsequencesParser.editTokenExpr: buildEditToken,
            ConsequencesParser.removeTokenExpr: buildRemoveToken,
            ConsequencesParser.printExpr: buildPrintExpr,
            ConsequencesParser.arithmExpr: buildArithmetic
        }

        return exprSymbols[rootName]()

    @classmethod
    def buildArithmeticExpression(cls, tree):
        rootName = tree[0]

        def buildNext():
            return cls.buildArithmeticExpression(tree[1])

        def buildDoubleNext():
            return cls.buildArithmeticExpression(tree[2])

        def stringWithoutQuotes():
            return ALitteral(tree[1][1:-1])

        def intvalue():
            return ALitteral(int(tree[1]))

        def floatvalue():
            return ALitteral(float(tree[1]))

        def variableValue():
            return ALitteral(Variable(tree[1]))

        def selfVariableValue():
            return SelfExpression()

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

        def buildMinExpression():
            x1 = cls.buildArithmeticExpression(tree[3])
            x2 = cls.buildArithmeticExpression(tree[5])
            return Min(x1, x2)

        def buildMaxExpression():
            x1 = cls.buildArithmeticExpression(tree[3])
            x2 = cls.buildArithmeticExpression(tree[5])
            return Max(x1, x2)

        arithmeticSymbols = {
            ConsequencesParser.arithmExpr: buildNext,
            ConsequencesParser.parArithmExpr: buildDoubleNext,
            ConsequencesParser.T.integer: intvalue,
            ConsequencesParser.T.float: floatvalue,
            ConsequencesParser.T.variable: variableValue,
            ConsequencesParser.T.selfvariable: selfVariableValue,
            ConsequencesParser.T.string: stringWithoutQuotes,
            ConsequencesParser.listExpr: listValue,
            ConsequencesParser.linkedListExpr: linkedListValue,
            ConsequencesParser.setExpr: setValue,
            ConsequencesParser.getItemArithExpr: buildGetItemExpression,
            ConsequencesParser.getSublistArithExpr: buildGetSublistExpression,
            ConsequencesParser.insertArithExpr: buildInsertExpression,
            ConsequencesParser.removeArithExpr: buildRemoveExpression,
            ConsequencesParser.addArithExpr: buildBinaryExpression,
            ConsequencesParser.minusArithExpr: buildMinusExpression,
            ConsequencesParser.multArithExpr: buildBinaryExpression,
            ConsequencesParser.powerArithExpr: buildBinaryExpression,
            ConsequencesParser.constantExpr: buildConstant,
            ConsequencesParser.funcExpr: buildFunctionExpression,
            ConsequencesParser.minExpr: buildMinExpression,
            ConsequencesParser.maxExpr: buildMaxExpression
        }

        return arithmeticSymbols[rootName]()


if __name__ == '__main__':
    print ConsequencesParser.pre_compile_grammar()
    expr = 'print min(3,5+3)'
    print ConsequencesParser.parse(expr)
