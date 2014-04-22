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

    def tick(self):
        def transitionOf(n):
            for transition in n.outputArcs:
                evaluation = transition.eval()
                if evaluation is None:
                    continue
                return transition, transition.consequences(evaluation)

        transitionGen = (transitionOf(n) for n in self._activeStates)
        transitionGen2 = [trcs for trcs in transitionGen if not trcs is None]

        self._activeStates.difference_update(trcs[0].n1 for trcs in transitionGen2)

        def newActiveState(transition):
            node = transition.n2
            node.init()
            return node

        self._activeStates.update(newActiveState(trcs[0]) for trcs in transitionGen2)

        Property.properties.update(chain(*(trcs[1][0] for trcs in transitionGen2)))
        Property.properties.difference_update(chain(*(trcs[1][1] for trcs in transitionGen2)))

        Event.events.clear()
        Event.events.update(chain(*(trcs[1][2] for trcs in transitionGen2)))

        for trcs in transitionGen2:
            for addSprite in trcs[1][3]:
                gameWindow.addSprite(addSprite.name, addSprite.num, addSprite.x, addSprite.y)
            for removeSprite in trcs[1][4]:
                gameWindow.removeSprite(removeSprite.name)
            for moveSprite in trcs[1][5]:
                gameWindow.moveSprite(moveSprite.name, moveSprite.dx, moveSprite.dy)
            for editSprite in trcs[1][6]:
                gameWindow.editSprite(editSprite.name, editSprite.num)

        print self._activeStates, Property.properties, Event.events


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
        for evaluation in self._trigger.eval():
            return evaluation

    def consequences(self, evaluation):
        consParsed = (ConsequencesParser.parse(cons) for cons in self._consequences)
        consEvaluated = [(consType, cons.eval_update(evaluation)) for consType, cons in consParsed]
        pToAdd = (cons for consType, cons in consEvaluated if consType == ADD_CONSEQUENCE
                  and isinstance(cons, Property))
        pToRemove = (cons for consType, cons in consEvaluated if consType == REMOVE_CONSEQUENCE
                     and isinstance(cons, Property))
        eToAdd = (cons for consType, cons in consEvaluated if consType == ADD_CONSEQUENCE and isinstance(cons, Event))
        spToAdd = (cons for consType, cons in consEvaluated if consType == ADD_SPRITE_CONSEQUENCE)
        spToRemove = (cons for consType, cons in consEvaluated if consType == REMOVE_SPRITE_CONSEQUENCE)
        spToMove = (cons for consType, cons in consEvaluated if consType == MOVE_SPRITE_CONSEQUENCE)
        spToEdit = (cons for consType, cons in consEvaluated if consType == EDIT_SPRITE_CONSEQUENCE)
        return pToAdd, pToRemove, eToAdd, spToAdd, spToRemove, spToMove, spToEdit

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