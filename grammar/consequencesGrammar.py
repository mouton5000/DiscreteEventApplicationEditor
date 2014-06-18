import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token, Opt
from booleanExpressions import Property, Event

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

    parameters = List(T.string | T.variable | T.integer | T.float, Token(','))
    propExpr = T.prop + '(' + parameters + ')'
    eventExpr = T.event + '(' + parameters + ')'

    addExpr = T.add + (propExpr | eventExpr)
    removeExpr = T.remove + propExpr

    addTokenExpr = T.add + T.token + '(' + T.integer + Opt(',' + parameters) + ')'
    editTokenExpr = T.edit + T.token + '(' + Opt(parameters) + ')'
    removeTokenExpr = T.remove + T.token

    addSpriteExpr = T.add + T.sprite + '(' + (T.string | T.variable) + ',' + (T.integer | T.variable) + ',' + \
                    (T.integer | T.variable) + ',' + (T.integer | T.variable) + ')'
    editSpriteExpr = T.edit + T.sprite + '(' + (T.string | T.variable) + ',' + (T.integer | T.variable) + ')'
    removeSpriteExpr = T.remove + T.sprite + '(' + (T.string | T.variable) + ')'
    moveSpriteExpr = T.move + T.sprite + '(' + (T.string | T.variable) + ',' + (T.integer | T.variable) + ',' + \
                     (T.integer | T.variable) + ')'

    consExpr = Prio(addExpr, removeExpr, addSpriteExpr, removeSpriteExpr, moveSpriteExpr, editSpriteExpr, addTokenExpr,
                    editTokenExpr, removeTokenExpr)

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
            return Property(name, *args)

        def buildEvent():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return Event(name, *args)

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

        def buildParameters():
            return (cls.buildExpression(arg) for arg in tree[1::2])

        exprSymbols = {
            ConsequencesParser.START: buildNext,
            ConsequencesParser.consExpr: buildNext,
            ConsequencesParser.addExpr: buildAdd,
            ConsequencesParser.removeExpr: buildRemove,
            ConsequencesParser.propExpr: buildProperty,
            ConsequencesParser.eventExpr: buildEvent,
            ConsequencesParser.T.event: value,
            ConsequencesParser.T.prop: value,
            ConsequencesParser.T.variable: value,
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
            ConsequencesParser.removeTokenExpr: buildRemoveToken
        }

        return exprSymbols[rootName]()


class SpriteConsequence(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


def _evalArg(arg, evaluation):
    try:
        return evaluation[arg]
    except KeyError:
        return arg


class AddSpriteConsequence(SpriteConsequence):
    def __init__(self, name, num, x, y):
        super(AddSpriteConsequence, self).__init__(name)
        self._num = num
        self._x = x
        self._y = y

    def eval_update(self, evaluation):
        name = _evalArg(self._name, evaluation)
        num = _evalArg(self._num, evaluation)
        x = _evalArg(self._x, evaluation)
        y = _evalArg(self._y, evaluation)
        return AddSpriteConsequence(name, num, x, y)

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
        name = _evalArg(self._name, evaluation)
        return RemoveSpriteConsequence(name)


class MoveSpriteConsequence(SpriteConsequence):
    def __init__(self, name, dx, dy):
        super(MoveSpriteConsequence, self).__init__(name)
        self._dx = dx
        self._dy = dy

    def eval_update(self, evaluation):
        name = _evalArg(self._name, evaluation)
        dx = _evalArg(self._dx, evaluation)
        dy = _evalArg(self._dy, evaluation)

        return MoveSpriteConsequence(name, dx, dy)

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
        name = _evalArg(self._name, evaluation)
        num = _evalArg(self._num, evaluation)

        return EditSpriteConsequence(name, num)

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
        nodeNum = _evalArg(self._nodeNum, evaluation)
        newParameters = (_evalArg(arg, evaluation) for arg in self._parameters)

        return AddTokenConsequence(nodeNum, *newParameters)


class EditTokenConsequence(object):
    def __init__(self, *args):
        self._parameters = args

    @property
    def parameters(self):
        return self._parameters

    def eval_update(self, evaluation):
        newParameters = (_evalArg(arg, evaluation) for arg in self._parameters)
        return EditTokenConsequence(*newParameters)


class RemoveTokenConsequence(object):
    def __init__(self):
        pass

    def eval_update(self, _):
        return self

if __name__ == '__main__':
    expr = 'A token(1)'
    print ConsequencesParser.parse(expr)
