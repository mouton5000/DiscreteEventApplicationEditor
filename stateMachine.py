# NO EXPORT

from grammar.triggerGrammar import TriggerParser
from grammar.triggerExpressions import BExpression
from grammar.consequenceGrammar import ConsequenceParser

# EXPORT

import database
from database import Property, Event, \
    SpriteProperty, TextProperty, LineProperty, \
    OvalProperty, RectProperty, PolygonProperty, \
    Variable
from lrparsing import LrParsingError


class TransitionTriggerParserException(Exception):
    def __init__(self, tr, trigger, parseError):
        super(TransitionTriggerParserException, self).__init__(
            TransitionTriggerParserException.getMessage(tr, trigger, parseError))

    @staticmethod
    def getMessage(tr, trigger, parseError):
        s1 = 'Error while parsing trigger of transition between ' + str(tr.n1.num) + ' and ' + str(tr.n2.num)
        s2 = 'Trigger : ' + trigger
        s3 = str(parseError)
        return s1 + '\n' + s2 + '\n' + s3


class TransitionConsequenceParserException(Exception):
    def __init__(self, tr, consequence, parseError):
        super(TransitionConsequenceParserException, self).__init__(
            TransitionConsequenceParserException.getMessage(tr, consequence, parseError))

    @staticmethod
    def getMessage(tr, consequence, parseError):
        if tr is None:
            s1 = 'Error while parsing init consequences'
        else:
            s1 = 'Error while parsing consequences of transition between ' + str(tr.n1.num) + ' and ' + str(tr.n2.num)
        s2 = 'Consequence : ' + consequence
        s3 = str(parseError)
        return s1 + '\n' + s2 + '\n' + s3


def _parseConsequence(consequence, transition):
    try:
        return ConsequenceParser.parse(consequence)
    except LrParsingError as consequenceParseError:
        raise TransitionConsequenceParserException(transition, consequence, consequenceParseError)


_tokens = set([])
_nodes = {}
i = 0


def clear():
    global _tokens, _nodes, i
    _tokens = set([])
    _nodes = {}
    i = 0


def addTokenByNodeNum(nodeNum, variables):
    node = getNodeByNum(nodeNum)
    token = Token(node)
    for variable, value in variables.iteritems():
        token.evaluation[variable] = value
    _tokens.add(token)


def removeToken(token):
    _tokens.remove(token)


def removeAllToken():
    _tokens.clear()


def clearTokens():
    _tokens.clear()


def getTokens():
    return _tokens


def updateTokensNbFrames():
    for token in _tokens:
        token.oneMoreFrame()


def addNode(num, label):
    node = Node(num, label)
    _nodes[num] = node
    return node


def getNodes():
    return _nodes.values()


def getNodeByNum(num):
    return _nodes[num]


def clearNodes():
    _nodes.clear()


def init():
    reinit()


def reinit():
    clearTokens()
    database.reinit()


def applyInitConsequences(initConsequences):
    parsedConsequences = (_parseConsequence(consequence, None) for consequence in initConsequences)
    for parsedCons in parsedConsequences:
            parsedCons.eval_update(Evaluation(), None)


def tick(debug=False):
    if debug:
        print 'Tokens : ', _tokens
        print 'Properties : ', Property.properties
        print 'Events : ', Event.events
        print 'Sprites : ', SpriteProperty.sprites
        print 'Texts : ', TextProperty.texts
        print 'Lines : ', LineProperty.lines
        print 'Ovals : ', OvalProperty.ovals
        print 'Rects : ', RectProperty.rects
        print 'Polygons : ', PolygonProperty.polygons
        print
    from itertools import chain

    # bug? la variable token est iteree a partir de la liste tokens
    # cependant la variable token dans les valeurs chain.from ... token.node.outputArcs)
    # est toujours egale au premier token alors que la cles est iteree correctement
    # On se retrouve donc avec le dictionnaire suivant :
    # {token1 : chain...(token1), token2 : chain...(token1), token3 : chain...(token1), ...}
    # tokenEvaluations = {token: chain.from_iterable(((evaluation, tr) for evaluation in tr.eval(token))
    #                                               for tr in token.node.outputArcs) for token in tokens}

    # la version suivant fonctionne correctement
    # tokenTransitionArcs = {token: iter(token.node.outputArcs) for token in self._tokens}
    # tokenEvaluations = {}
    # for token in self._tokens:
    #     try:
    #         transitionArc = tokenTransitionArcs[token].next()
    #         tokenEvaluations[token] = transitionArc.eval(token)
    #     except StopIteration:
    #         pass
    #
    #
    # transitionGen = {}

    locks = {}
    tokensEvaluations = {}

    tokenTransitionArcIterator = {token: iter(token.node.outputArcs) for token in _tokens}
    toCheck = _tokens

    def checkLock(locks, keys, prio, toRecheck, tokensEvaluations, token):
        try:
            if locks[keys][0] > prio:
                toRecheck |= locks[keys][1]
                for token2 in locks[keys][1]:
                    del tokensEvaluations[token2]
                locks[keys] = (prio, set([token]))
            elif locks[keys][0] == prio:
                locks[keys][1].add(token)
            else:
                return True
        except KeyError:
            locks[keys] = (prio, set([token]))
        return False

    while len(toCheck) > 0:
        toRecheck = set([])

        for token in toCheck:
            try:
                transition = tokenTransitionArcIterator[token].next()
            except StopIteration:
                continue

            tokenEvaluations = transition.eval(token)
            try:
                evaluation = tokenEvaluations.next()
            except StopIteration:
                toRecheck.add(token)
                continue

            tokenEvaluations = [evaluation] + list(tokenEvaluations)
            tokenLocks = chain.from_iterable(((keys, prio) for keys, prio in evaluation.locks.iteritems())
                                             for evaluation in tokenEvaluations)

            locked = False

            try:
                keys, prio = tokenLocks.next()
                locked |= checkLock(locks, keys, prio, toRecheck, tokensEvaluations, token)

            except StopIteration:
                tokensEvaluations[token] = (transition, tokenEvaluations)
                continue

            for keys, prio in tokenLocks:
                locked |= checkLock(locks, keys, prio, toRecheck, tokensEvaluations, token)

            if locked:
                toRecheck.add(token)
            else:
                tokensEvaluations[token] = (transition, tokenEvaluations)

        toCheck = toRecheck

    # toCheck = self._tokens
    # while len(toCheck) > 0:
    #     toRecheck = set([])
    #     for token in toCheck:
    #         evaluations = tokenEvaluations[token]
    #         try:
    #             evaluation, tr = evaluations.next()
    #             locked = False
    #             if len(evaluation.locks) > 0:
    #                 for keys, prio in evaluation.locks.iteritems():
    #                     try:
    #                         if locks[keys][0] > prio:
    #                             toRecheck |= locks[keys][1]
    #                             for token2 in locks[keys][1]:
    #                                 del transitionGen[token2]
    #                             locks[keys] = (prio, set([token]))
    #                         elif locks[keys][0] == prio:
    #                             locks[keys][1].add(token)
    #                         else:
    #                             locked = True
    #                     except KeyError:
    #                         locks[keys] = (prio, set([token]))
    #             if locked:
    #                 toRecheck.add(token)
    #             else:
    #                 transitionGen[token] = (tr, evaluation.variables)
    #         except StopIteration:
    #             pass
    #     toCheck = toRecheck
    # Event.events.clear()

    # if len(transitionGen) == 0:
    #     return False
    #
    # for token in transitionGen:
    #     tr, evaluation = transitionGen[token]
    #     token.moveTo(tr.n2)
    #     tr.applyConsequences(evaluation, self, token)

    Event.events.clear()
    if len(tokensEvaluations) == 0:
        return False

    if debug:
        print 'Tokens :'
        for token in tokensEvaluations:
            print token, tokensEvaluations[token]

        print

    for token in tokensEvaluations:
        tr, evaluations = tokensEvaluations[token]
        token.moveTo(tr.n2)
        for evaluation in evaluations:
            tr.applyConsequences(evaluation, token)

    return True


class Evaluation(object):
    def __init__(self):
        self.variables = dict()
        self.locks = dict()

    def __getitem__(self, key):
        if isinstance(key, Variable):
            return self.variables[key]
        else:
            return self.locks[key]

    def __setitem__(self, key, value):
        if isinstance(key, Variable):
            self.variables[key] = value
        else:
            self.locks[key] = value

    def __str__(self):
        return str(self.variables) + ' ' + str(self.locks)

    def __repr__(self):
        return str(self)

    def copy(self):
        e = Evaluation()
        e.variables = self.variables.copy()
        e.locks = self.locks.copy()
        return e

    def __contains__(self, key):
        if isinstance(key, Variable):
            return key in self.variables
        else:
            return key in self.locks

    def __delitem__(self, key):
        if isinstance(key, Variable):
            del self.variables[key]
        else:
            del self.locks[key]

    def __len__(self):
        return len(self.variables) + len(self.locks)

    def popitem(self):
        try:
            return self.variables.popitem()
        except KeyError:
            return self.locks.popitem()

    def __eq__(self, other):
        return self.variables == other.variables and self.locks == other.locks


class Token(object):
    def __init__(self, node):
        self._node = node
        self._nbFrameSinceLastMove = 0
        self.evaluation = Evaluation()

    @property
    def node(self):
        return self._node

    def moveTo(self, node):
        self._node = node
        self._nbFrameSinceLastMove = 0

    def oneMoreFrame(self):
        self._nbFrameSinceLastMove += 1

    @property
    def nbFrameSinceLastMove(self):
        return self._nbFrameSinceLastMove

    def __str__(self):
        s = super(Token, self).__str__()
        return '(' + str(self._node.num) + ',' + str(self._nbFrameSinceLastMove) + ',' + s + ')'

    def __repr__(self):
        return str(self)


class Node:
    def __init__(self, num, name):
        self.outputArcs = []
        self._num = num
        self._name = name

    @property
    def num(self):
        return self._num

    @property
    def name(self):
        return self._name

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)


class Transition:
    def __init__(self, in1, in2, trigger, consequences, parse=True):
        self.n1 = in1
        in1.outputArcs.append(self)
        self.n2 = in2

        if parse:
            try:
                self._trigger = BExpression(TriggerParser.parse(trigger))
            except LrParsingError as triggerParseError:
                raise TransitionTriggerParserException(self, trigger, triggerParseError)

            def parseConsequence(consequence):
                try:
                    return ConsequenceParser.parse(consequence)
                except LrParsingError as consequenceParseError:
                    raise TransitionConsequenceParserException(self, consequence, consequenceParseError)

            self._consequences = [parseConsequence(cons) for cons in consequences]
        else:
            self._trigger = trigger
            self._consequences = consequences

    def eval(self, token):
        return self._trigger.eval(token)

    def applyConsequences(self, evaluation, token):
        for parsedCons in self._consequences:
            parsedCons.eval_update(evaluation, token)

    def exportFormula(self):
        return self._trigger.export()

    def exportConsequences(self):
        return '[' + ','.join(parsedCons.export() for parsedCons in self._consequences) + ']'

    def __str__(self):
        return str(self.n1) + ' ' + str(self.n2)

    def __repr__(self):
        return str(self.n1) + ' ' + str(self.n2)