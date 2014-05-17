from itertools import chain

from grammar.grammar import BooleanExpressionParser
from grammar.booleanExpressions import BExpression, Property, Event
from grammar.consequencesGrammar import ConsequencesParser, ADD_CONSEQUENCE, REMOVE_CONSEQUENCE, \
    ADD_SPRITE_CONSEQUENCE, REMOVE_SPRITE_CONSEQUENCE, MOVE_SPRITE_CONSEQUENCE, EDIT_SPRITE_CONSEQUENCE

import game.gameWindow as gameWindow


class StateMachine:
    def __init__(self):
        self._activeStates = set([])

    def addActiveState(self, n):
        self._activeStates.add(n)

    def clearActiveStates(self):
        self._activeStates.clear()

    def init(self):
        for n in self._activeStates:
            n.init()

    def tick(self):

        print self._activeStates, Property.properties, Event.events

        from collections import deque
        nodes = deque(node for node in self._activeStates)

        def nodesGenerator():
            # Il y a peut-etre mieux.
            try:
                while True:
                    yield nodes.pop()
            except IndexError:
                pass

        from itertools import chain
        nodeEvaluations = {node: chain.from_iterable(((evaluation, tr) for evaluation in tr.eval())
                                                     for tr in node.outputArcs) for node in nodes}

        locks = {}

        transitionGen = {}
        for node in nodesGenerator():
            evaluations = nodeEvaluations[node]
            for evaluation, tr in evaluations:
                if len(evaluation.locks) > 0:
                    if any(keys in locks and locks[keys][0] <= prio for keys, prio in evaluation.locks.iteritems()):
                        continue
                    toAdd = set([])
                    for keys, prio in evaluation.locks.iteritems():
                        if keys in locks:
                            toAdd.add(locks[keys][1])
                        locks[keys] = (prio, node)
                    nodes.extend(toAdd)
                    for n in toAdd:
                        del transitionGen[n]
                    print locks
                transitionGen[node] = (tr, tr.consequences(evaluation.variables))
                break

        # TODO sera ameliore plus tard

        self._activeStates.difference_update(node for node in transitionGen)

        def newActiveState(transition):
            node = transition.n2
            node.init()
            return node

        self._activeStates.update(newActiveState(transitionGen[node][0]) for node in transitionGen)

        Event.events.clear()
        for node in transitionGen:
            trans, consequences = transitionGen[node]
            for consType, cons in consequences:
                if consType == ADD_CONSEQUENCE and isinstance(cons, Property):
                    Property.properties.add(cons)
                elif consType == REMOVE_CONSEQUENCE and isinstance(cons, Property):
                    try:
                        Property.properties.remove(cons)
                    except KeyError:
                        pass
                elif consType == ADD_CONSEQUENCE and isinstance(cons, Event):
                    Event.events.add(cons)
                elif consType == ADD_SPRITE_CONSEQUENCE:
                    gameWindow.addSprite(cons.name, cons.num, cons.x, cons.y)
                elif consType == REMOVE_SPRITE_CONSEQUENCE:
                    try:
                        gameWindow.removeSprite(cons.name)
                    except KeyError:
                        pass
                elif consType == MOVE_SPRITE_CONSEQUENCE:
                    try:
                        gameWindow.moveSprite(cons.name, cons.dx, cons.dy)
                    except KeyError:
                        pass
                elif consType == EDIT_SPRITE_CONSEQUENCE:
                    try:
                        gameWindow.editSprite(cons.name, cons.num)
                    except KeyError:
                        pass


class Node:
    def __init__(self, name):
        self.outputArcs = []
        self._name = name

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)

    def init(self):
        for transition in self.outputArcs:
            transition.init()


class Transition:
    def __init__(self, in1, in2, trigger, consequences):
        self.n1 = in1
        in1.outputArcs.append(self)
        self.n2 = in2
        self._trigger = BExpression(BooleanExpressionParser.parse(trigger))
        self._consequences = consequences

    def init(self):
        self._trigger.init()

    def eval(self):
        return self._trigger.eval()

    def consequences(self, evaluation):
        consParsed = (ConsequencesParser.parse(cons) for cons in self._consequences)
        return ((consType, cons.eval_update(evaluation)) for consType, cons in consParsed)

    def __str__(self):
        return str(self.n1) + ' ' + str(self.n2)

    def __repr__(self):
        return str(self.n1) + ' ' + str(self.n2)


if __name__ == '__main__':
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)

    f1 = 'true'
    Transition(n1, n2, f1, ['A pW(0,0)', 'A pW(0,1)', 'A pW(0,2)'])

    f2 = 'pW(X,3)'
    Transition(n2, n3, f2, ['A pW(X,1)', 'R pW(X,3)'])

    f3 = 'pW(X,1)'
    Transition(n2, n2, f3, ['A pW(X,3)', 'R pW(X,1)'])

    f4 = 'pW(X,1)'
    Transition(n3, n2, f4, ['A pW(X,3)', 'R pW(X,1)'])

    sm = StateMachine()
    sm.addActiveState(n1)

    for i in xrange(10):
        print sm._activeStates, Property.properties, Event.events
        sm.tick()