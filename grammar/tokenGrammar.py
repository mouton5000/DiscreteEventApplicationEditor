__author__ = 'mouton'

import lrparsing
from lrparsing import List, Prio, Ref, Token


class TokenParametersParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='-?[0-9]+')
        float = Token(re='-?[0-9]+\.[0-9]+')
        string = Token(re='\'[A-Za-z_0-9]*\'')

    consExpr = Ref('consExpr')

    parameters = List(T.string | T.integer | T.float, Token(','))
    consExpr = Prio(parameters)

    START = consExpr

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(TokenParametersParser, cls).parse(expr, tree_factory, on_error, log)
        return cls.buildToken(tree)

    @classmethod
    def buildToken(cls, tree):
        rootName = tree[0]

        def build():
            return cls.buildToken(tree[1])

        def stringWithoutQuotes():
            return tree[1][1:-1]

        def intvalue():
            return int(tree[1])

        def floatvalue():
            return float(tree[1])

        def buildParameters():
            return [cls.buildToken(arg) for arg in tree[1::2]]

        tokenSymbols = {
            TokenParametersParser.START: build,
            TokenParametersParser.consExpr: build,
            TokenParametersParser.T.string: stringWithoutQuotes,
            TokenParametersParser.T.integer: intvalue,
            TokenParametersParser.T.float: floatvalue,
            TokenParametersParser.parameters: buildParameters,

        }

        return tokenSymbols[rootName]()