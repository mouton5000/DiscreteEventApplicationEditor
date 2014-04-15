import lrparsing
from lrparsing import Keyword, List, Prio, Ref, Token
from booleanExpressions import Property, Event


class ConsequencesParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='[0-9]+')
        float = Token(re='[0-9]+\.[0-9]+')
        string = Token(re='\'[A-Za-z_0-9]*\'')
        variable = Token(re='[A-Z][A-Z_0-9]*')
        prop = Token(re='p[A-Z][A-Za-z_0-9]*')
        event = Token(re='e[A-Z][A-Za-z_0-9]*')
        add = Keyword('A')
        remove = Keyword('R')

    consExpr = Ref('consExpr')

    parameters = List(T.string | T.variable | T.integer | T.float, Token(','))
    propExpr = T.prop + '(' + parameters + ')'
    eventExpr = T.event + '(' + parameters + ')'

    addExpr = T.add + (propExpr | eventExpr)
    removeExpr = T.remove + propExpr

    consExpr = Prio(addExpr, removeExpr)

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
            return True, cls.buildExpression(tree[2])

        def buildRemove():
            return False, cls.buildExpression(tree[2])

        def buildProperty():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return Property(name, *args)

        def buildEvent():
            name = cls.buildExpression(tree[1])[1:]
            args = cls.buildExpression(tree[3])
            return Event(name, *args)

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
            ConsequencesParser.parameters: buildParameters
        }

        return exprSymbols[rootName]()