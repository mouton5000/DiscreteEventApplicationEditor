from grammar.grammar import BooleanExpressionParser
from grammar.booleanExpressions import BExpression
from grammar.consequencesGrammar import ConsequencesParser
from grammar.tokenGrammar import TokenParametersParser
from database import Property, Event, UNDEFINED_PARAMETER
from lrparsing import LrParsingError


class TokenParseException(Exception):
    def __init__(self, node, tokenText, parseError):
        super(TokenParseException, self).__init__(
            TokenParseException.getMessage(node, tokenText, parseError))

    @staticmethod
    def getMessage(node, tokenText, parseError):
        s1 = 'Error while parsing token of node ' + str(node.num)
        s2 = 'Token text : ' + tokenText
        s3 = str(parseError)
        return s1 + '\n' + s2 + '\n' + s3


class StateMachine:
    def __init__(self):
        self._tokens = set([])
        self._nodes = {}
        self.i = 0
        self.gameWindow = None

    def setGameWindow(self, gw):
        self.gameWindow = gw

    def addTokenByNodeNum(self, nodeNum, parameters):
        node = self.getNodeByNum(nodeNum)
        token = Token(node, parameters)
        self._tokens.add(token)

    def addToken(self, node, tokenStr):
        try:
            token = Token(node, TokenParametersParser.parse(tokenStr))
        except LrParsingError as e:
            raise TokenParseException(node, tokenStr, e)
        self._tokens.add(token)

    def removeToken(self, token):
        self._tokens.remove(token)

    def clearTokens(self):
        self._tokens.clear()

    def updateTokensNbFrames(self):
        for token in self._tokens:
            token.oneMoreFrame()

    def addNode(self, num, label):
        node = Node(num, label)
        self._nodes[num] = node
        return node

    def getNodeByNum(self, num):
        return self._nodes[num]

    def clearNodes(self):
        self._nodes.clear()

    def init(self):
        self.clearTokens()
        Property.properties.clear()
        Event.events.clear()

    def tick(self):
        print self._tokens, Property.properties, Event.events
        from itertools import chain

        # bug? la variable token est iteree a partir de la liste tokens
        # cependant la variable token dans les valeurs chain.from ... token.node.outputArcs)
        # est toujours egale au premier token alors que la cles est iteree correctement
        # On se retrouve donc avec le dictionnaire suivant :
        # {token1 : chain...(token1), token2 : chain...(token1), token3 : chain...(token1), ...}
        # tokenEvaluations = {token: chain.from_iterable(((evaluation, tr) for evaluation in tr.eval(token))
        #                                               for tr in token.node.outputArcs) for token in tokens}

        # la version suivant fonctionne correctement
        tokenEvaluations = {}
        for token in self._tokens:
            tokenEvaluations[token] = chain.from_iterable(((evaluation, tr) for evaluation in tr.eval(token))
                                                          for tr in token.node.outputArcs)

        locks = {}
        transitionGen = {}

        toCheck = self._tokens
        while len(toCheck) > 0:
            toRecheck = set([])
            for token in toCheck:
                evaluations = tokenEvaluations[token]
                try:
                    evaluation, tr = evaluations.next()
                    locked = False
                    if len(evaluation.locks) > 0:
                        for keys, prio in evaluation.locks.iteritems():
                            try:
                                if locks[keys][0] > prio:
                                    toRecheck |= locks[keys][1]
                                    for token2 in locks[keys][1]:
                                        del transitionGen[token2]
                                    locks[keys] = (prio, set([token]))
                                elif locks[keys][0] == prio:
                                    locks[keys][1].add(token)
                                else:
                                    locked = True
                            except KeyError:
                                locks[keys] = (prio, set([token]))
                    if locked:
                        toRecheck.add(token)
                    else:
                        transitionGen[token] = (tr, evaluation.variables)
                except StopIteration:
                    pass
            toCheck = toRecheck
        Event.events.clear()

        if len(transitionGen) == 0:
            return False

        for token in transitionGen:
            tr, evaluation = transitionGen[token]
            token.moveTo(tr.n2)
            tr.applyConsequences(evaluation, self, token)
            # for consType, cons in consequences:
            #     if cons is None:
            #         continue
            #     if consType == ADD_PROPERTY_CONSEQUENCE:
            #         prop = Property(cons[0], cons[1])
            #         Property.properties.add(prop)
            #     elif consType == REMOVE_PROPERTY_CONSEQUENCE:
            #         Property.removeAll(cons[0], cons[1])
            #     elif consType == EDIT_PROPERTY_CONSEQUENCE:
            #         Property.edit(cons[0], cons[1], cons[2])
            #     elif consType == ADD_EVENT_CONSEQUENCE:
            #         event = Event(cons[0], cons[1])
            #         Event.events.add(event)
            #     elif consType == ADD_SPRITE_CONSEQUENCE:
            #         gameWindow.addSprite(cons[0], cons[1], cons[2], cons[3])
            #     elif consType == REMOVE_SPRITE_CONSEQUENCE:
            #         try:
            #             gameWindow.removeSprite(cons)
            #         except KeyError:
            #             pass
            #     elif consType == MOVE_SPRITE_CONSEQUENCE:
            #         try:
            #             gameWindow.moveSprite(cons[0], cons[1], cons[2])
            #         except KeyError:
            #             pass
            #     elif consType == EDIT_SPRITE_CONSEQUENCE:
            #         try:
            #             gameWindow.editSprite(cons[0], cons[1])
            #         except KeyError:
            #             pass
            #     elif consType == ADD_TOKEN_CONSEQUENCE:
            #         node = self.getNodeByNum(cons[0])
            #         newToken = Token(node, cons[1])
            #         self._tokens.add(newToken)
            #     elif consType == EDIT_TOKEN_CONSEQUENCE:
            #         token.setArgs(cons)
            #     elif consType == REMOVE_TOKEN_CONSEQUENCE:
            #         self.removeToken(token)
        return True


class Token:
    def __init__(self, node, args):
        self._node = node
        self._args = args
        self._nbFrameSinceLastMove = 0

    @property
    def node(self):
        return self._node

    def setArgs(self, unevaluatedArgs, evaluation):
        def evalArg(uArg, tArg):
            if uArg is None:
                return
            value = uArg.value(evaluation, selfParam=tArg)
            if value == UNDEFINED_PARAMETER:
                value = tArg
            return value

        newArgs = (evalArg(unevaluatedArg, arg) for unevaluatedArg, arg in map(None, unevaluatedArgs, self))
        self._args[:] = [arg for arg in newArgs if arg is not None]

    def moveTo(self, node):
        self._node = node
        self._nbFrameSinceLastMove = 0

    def oneMoreFrame(self):
        self._nbFrameSinceLastMove += 1

    @property
    def nbFrameSinceLastMove(self):
        return self._nbFrameSinceLastMove

    def __iter__(self):
        return iter(self._args)

    def __getitem__(self, index):
        return self._args[index]

    def __str__(self):
        return 'Token(' + str(self.node) + ',' + str(self._nbFrameSinceLastMove) + ',' + ','.join([str(o)
                                                                                                   for o in
                                                                                                   self._args]) + ')'

    def __repr__(self):
        return 'Token(' + str(self.node) + ',' + str(self._nbFrameSinceLastMove) + ',' + ','.join([str(o)
                                                                                                   for o in
                                                                                                   self._args]) + ')'

    def __len__(self):
        return len(self._args)


class Node:
    def __init__(self, num, name):
        self.outputArcs = []
        self._num = num
        self._name = name

    @property
    def num(self):
        return self._num

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)


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
        s1 = 'Error while parsing consequence of transition between ' + str(tr.n1.num) + ' and ' + str(tr.n2.num)
        s2 = 'Consequence : ' + consequence
        s3 = str(parseError)
        return s1 + '\n' + s2 + '\n' + s3


class Transition:
    def __init__(self, in1, in2, trigger, consequences):
        self.n1 = in1
        in1.outputArcs.append(self)
        self.n2 = in2

        try:
            self._trigger = BExpression(BooleanExpressionParser.parse(trigger))
        except LrParsingError as triggerParseError:
            raise TransitionTriggerParserException(self, trigger, triggerParseError)

        def parseConsequence(consequence):
            try:
                return ConsequencesParser.parse(consequence)
            except LrParsingError as consequenceParseError:
                raise TransitionConsequenceParserException(self, consequence, consequenceParseError)

        self._consequences = [parseConsequence(cons) for cons in consequences]

    def eval(self, token):
        return self._trigger.eval(token)

    def applyConsequences(self, evaluation, stateMachine, token):
        for parsedCons in self._consequences:
            parsedCons.eval_update(evaluation, stateMachine, token)

    def __str__(self):
        return str(self.n1) + ' ' + str(self.n2)

    def __repr__(self):
        return str(self.n1) + ' ' + str(self.n2)