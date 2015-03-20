__author__ = 'mouton'

import lrparsing
from lrparsing import List, Prio, Opt, Token


class TokenParametersParser(lrparsing.Grammar):
    class T(lrparsing.TokenRegistry):
        integer = Token(re='-?[0-9]+')
        float = Token(re='-?[0-9]+\.[0-9]+')
        string = Token(re='\'[A-Za-z_0-9]*\'')

    parameter = T.string | T.integer | T.float
    namedParameter = parameter + '=' + parameter
    parameters = \
        Prio(List(parameter, Token(',')) + Opt(',' + List(namedParameter, Token(','))),
             List(namedParameter, Token(',')))

    START = parameters

    @classmethod
    def parse(cls, expr, tree_factory=None, on_error=None, log=None):
        tree = super(TokenParametersParser, cls).parse(expr, tree_factory, on_error, log)
        return cls.buildToken(tree)

    @classmethod
    def buildToken(cls, tree):
        rootName = tree[0]

        def buildNext():
            return cls.buildToken(tree[1])

        def stringWithoutQuotes():
            return tree[1][1:-1]

        def intvalue():
            return int(tree[1])

        def floatvalue():
            return float(tree[1])

        def buildNamedParameter():
            name = cls.buildToken(tree[1])
            parameter = cls.buildToken(tree[3])
            return name, parameter

        def buildParameters():
            buildArgs = [cls.buildToken(arg) for arg in tree[1::2]]
            args = [arg for arg in buildArgs if not isinstance(arg, tuple)]
            kwargs = {kwarg[0]: kwarg[1] for kwarg in buildArgs if isinstance(kwarg, tuple)}
            return args, kwargs

        tokenSymbols = {
            TokenParametersParser.START: buildNext,
            # TokenParametersParser.consExpr: buildNext,
            TokenParametersParser.T.string: stringWithoutQuotes,
            TokenParametersParser.T.integer: intvalue,
            TokenParametersParser.T.float: floatvalue,
            TokenParametersParser.parameter: buildNext,
            TokenParametersParser.namedParameter: buildNamedParameter,
            TokenParametersParser.parameters: buildParameters
        }

        return tokenSymbols[rootName]()