import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token, Opt
from arithmeticExpressions import ALitteral, Addition, Subtraction, Product, Division, EuclideanDivision, Modulo, Power
from database import Variable, Property, Event

ADD_CONSEQUENCE = 0
REMOVE_CONSEQUENCE = 1
ADD_SPRITE_CONSEQUENCE = 2
REMOVE_SPRITE_CONSEQUENCE = 3
MOVE_SPRITE_CONSEQUENCE = 4
EDIT_SPRITE_CONSEQUENCE = 5
ADD_TOKEN_CONSEQUENCE = 6
EDIT_TOKEN_CONSEQUENCE = 7
REMOVE_TOKEN_CONSEQUENCE = 8


class ConsequencesParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='-?[0-9]+')
        float = Token(re='-?[0-9]+\.[0-9]+')
        string = Token(re='\'[A-Za-z_0-9]*\'')
        variable = Token(re='[A-Z][A-Z_0-9]*')
        prop = Token(re='p[A-Z][A-Za-z_0-9]*')
        event = Token(re='e[A-Z][A-Za-z_0-9]*')
        sprite = Token('s')
        token = Token('token')
        add = Keyword('A')
        remove = Keyword('R')
        move = Keyword('M')
        edit = Keyword('E')

    consExpr = Ref('consExpr')
    arithmExpr = Ref('arithmExpr')

    parameters = List(arithmExpr, Token(','))
    propExpr = T.prop + '(' + parameters + ')'
    eventExpr = T.event + '(' + parameters + ')'

    addExpr = T.add + (propExpr | eventExpr)
    removeExpr = T.remove + propExpr

    addTokenExpr = T.add + T.token + '(' + arithmExpr + Opt(',' + parameters) + ')'
    editTokenExpr = T.edit + T.token + '(' + Opt(parameters) + ')'
    removeTokenExpr = T.remove + T.token

    addSpriteExpr = T.add + T.sprite + '(' + arithmExpr + ',' + arithmExpr + ',' + \
                    arithmExpr + ',' + arithmExpr + ')'
    editSpriteExpr = T.edit + T.sprite + '(' + arithmExpr + ',' + arithmExpr + ')'
    removeSpriteExpr = T.remove + T.sprite + '(' + arithmExpr + ')'
    moveSpriteExpr = T.move + T.sprite + '(' + arithmExpr + ',' + arithmExpr + ',' + \
                     arithmExpr + ')'

    consExpr = Prio(addExpr, removeExpr, addSpriteExpr, removeSpriteExpr, moveSpriteExpr, editSpriteExpr, addTokenExpr,
                    editTokenExpr, removeTokenExpr)

    addArithExpr = arithmExpr << (Token('+') | Token('-')) << arithmExpr
    multArithExpr = arithmExpr << (Token('*') | Token('/') | Token('//') | Token('%')) << arithmExpr
    powerArithExpr = arithmExpr << Token('**') << arithmExpr
    parArithmExpr = '(' + arithmExpr + ')'

    arithmExpr = Prio(T.integer, T.float, T.variable, T.string, parArithmExpr, powerArithExpr, multArithExpr, addArithExpr)

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

        def buildAdd():
            return ADD_CONSEQUENCE, cls.buildExpression(tree[2])

        def buildRemove():
            return REMOVE_CONSEQUENCE, cls.buildExpression(tree[2])

        def buildAddSprite():
            name = cls.buildExpression(tree[4])
            num = cls.buildExpression(tree[6])
            x = cls.buildExpression(tree[8])
            y = cls.buildExpression(tree[10])
            return ADD_SPRITE_CONSEQUENCE, AddSpriteConsequence(name, num, x, y)

        def buildEditSprite():
            name = cls.buildExpression(tree[4])
            num = cls.buildExpression(tree[6])
            return EDIT_SPRITE_CONSEQUENCE, EditSpriteConsequence(name, num)

        def buildRemoveSprite():
            name = cls.buildExpression(tree[4])
            return REMOVE_SPRITE_CONSEQUENCE, RemoveSpriteConsequence(name)

        def buildMoveSprite():
            name = cls.buildExpression(tree[4])
            dx = cls.buildExpression(tree[6])
            dy = cls.buildExpression(tree[8])
            return MOVE_SPRITE_CONSEQUENCE, MoveSpriteConsequence(name, dx, dy)

        def buildProperty():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return PropertyConsequence(name, *args)

        def buildEvent():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return EventConsequence(name, *args)

        def buildAddToken():
            nodeNum = cls.buildExpression(tree[4])
            if len(tree) == 6:
                return ADD_TOKEN_CONSEQUENCE, AddTokenConsequence(nodeNum)
            else:
                args = cls.buildExpression(tree[6])
                return ADD_TOKEN_CONSEQUENCE, AddTokenConsequence(nodeNum, *args)

        def buildEditToken():
            if len(tree) == 5:
                return EDIT_TOKEN_CONSEQUENCE, EditTokenConsequence()
            else:
                args = cls.buildExpression(tree[4])
                return EDIT_TOKEN_CONSEQUENCE, EditTokenConsequence(*args)

        def buildRemoveToken():
            return REMOVE_TOKEN_CONSEQUENCE, RemoveTokenConsequence()

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

        def buildParameters():
            return (cls.buildExpression(arg) for arg in tree[1::2])

        def buildArithmetic():
            return cls.buildArithmeticExpression(tree)

        exprSymbols = {
            ConsequencesParser.START: buildNext,
            ConsequencesParser.consExpr: buildNext,
            ConsequencesParser.addExpr: buildAdd,
            ConsequencesParser.removeExpr: buildRemove,
            ConsequencesParser.propExpr: buildProperty,
            ConsequencesParser.eventExpr: buildEvent,
            ConsequencesParser.T.event: value,
            ConsequencesParser.T.prop: value,
            ConsequencesParser.T.variable: variableValue,
            ConsequencesParser.T.string: stringWithoutQuotes,
            ConsequencesParser.T.integer: intvalue,
            ConsequencesParser.T.float: floatvalue,
            ConsequencesParser.parameters: buildParameters,
            ConsequencesParser.addSpriteExpr: buildAddSprite,
            ConsequencesParser.removeSpriteExpr: buildRemoveSprite,
            ConsequencesParser.editSpriteExpr: buildEditSprite,
            ConsequencesParser.moveSpriteExpr: buildMoveSprite,
            ConsequencesParser.addTokenExpr: buildAddToken,
            ConsequencesParser.editTokenExpr: buildEditToken,
            ConsequencesParser.removeTokenExpr: buildRemoveToken,
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
            ConsequencesParser.arithmExpr: buildNext,
            ConsequencesParser.parArithmExpr: buildDoubleNext,
            ConsequencesParser.T.integer: buildLitteral,
            ConsequencesParser.T.float: buildLitteral,
            ConsequencesParser.T.variable: buildLitteral,
            ConsequencesParser.T.string: buildLitteral,
            ConsequencesParser.addArithExpr: buildBinaryExpression,
            ConsequencesParser.multArithExpr: buildBinaryExpression,
            ConsequencesParser.powerArithExpr: buildBinaryExpression
        }

        return arithmeticSymbols[rootName]()


class PropertyConsequence():

    def __init__(self, name, *args):
        self._name = name
        self._args = args

    def eval_update(self, evaluation):
        try:
            name = self._name
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            return Property(name, *newArgs)
        except (ArithmeticError, TypeError, ValueError):
            pass


class EventConsequence():
    events = set([])

    def __init__(self, name, *args):
        self._name = name
        self._args = args

    def eval_update(self, evaluation):
        try:
            name = self._name
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            return Event(name, *newArgs)
        except (ArithmeticError, TypeError, ValueError):
            pass


class SpriteConsequence(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


def _evalArg(arg, evaluation):
    return arg.value(evaluation)


class AddSpriteConsequence(SpriteConsequence):
    def __init__(self, name, num, x, y):
        super(AddSpriteConsequence, self).__init__(name)
        self._num = num
        self._x = x
        self._y = y

    def eval_update(self, evaluation):
        try:
            name = str(_evalArg(self._name, evaluation))
            num = int(_evalArg(self._num, evaluation))
            x = int(_evalArg(self._x, evaluation))
            y = int(_evalArg(self._y, evaluation))
            return AddSpriteConsequence(name, num, x, y)
        except (ArithmeticError, TypeError, ValueError):
            pass

    @property
    def num(self):
        return self._num

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class RemoveSpriteConsequence(SpriteConsequence):
    def __init__(self, name):
        super(RemoveSpriteConsequence, self).__init__(name)

    def eval_update(self, evaluation):
        try:
            name = str(_evalArg(self._name, evaluation))
            return RemoveSpriteConsequence(name)
        except (ArithmeticError, TypeError, ValueError):
            pass


class MoveSpriteConsequence(SpriteConsequence):
    def __init__(self, name, dx, dy):
        super(MoveSpriteConsequence, self).__init__(name)
        self._dx = dx
        self._dy = dy

    def eval_update(self, evaluation):
        try:
            name = str(_evalArg(self._name, evaluation))
            dx = int(_evalArg(self._dx, evaluation))
            dy = int(_evalArg(self._dy, evaluation))
            return MoveSpriteConsequence(name, dx, dy)
        except (ArithmeticError, TypeError, ValueError):
            pass

    @property
    def dx(self):
        return self._dx

    @property
    def dy(self):
        return self._dy


class EditSpriteConsequence(SpriteConsequence):
    def __init__(self, name, num):
        super(EditSpriteConsequence, self).__init__(name)
        self._num = num

    def eval_update(self, evaluation):
        try:
            name = str(_evalArg(self._name, evaluation))
            num = int(_evalArg(self._num, evaluation))
            return EditSpriteConsequence(name, num)
        except (ArithmeticError, TypeError, ValueError):
            pass

    @property
    def num(self):
        return self._num


class AddTokenConsequence(object):
    def __init__(self, nodeNum, *args):
        self._nodeNum = nodeNum
        self._parameters = args

    @property
    def nodeNum(self):
        return self._nodeNum

    @property
    def parameters(self):
        return self._parameters

    def eval_update(self, evaluation):
        try:
            nodeNum = int(_evalArg(self._nodeNum, evaluation))
            newParameters = (_evalArg(arg, evaluation) for arg in self._parameters)
            return AddTokenConsequence(nodeNum, *newParameters)
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditTokenConsequence(object):
    def __init__(self, *args):
        self._parameters = args

    @property
    def parameters(self):
        return self._parameters

    def eval_update(self, evaluation):
        try:
            newParameters = (_evalArg(arg, evaluation) for arg in self._parameters)
            return EditTokenConsequence(*newParameters)
        except (ArithmeticError, TypeError, ValueError):
            pass


class RemoveTokenConsequence(object):
    def __init__(self):
        pass

    def eval_update(self, _):
        return self

if __name__ == '__main__':
    expr = 'A token(1)'
    print ConsequencesParser.parse(expr)
