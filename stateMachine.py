from grammar import BooleanExpressionParser
from booleanExpressions import BExpression, Property, Event
from consequencesGrammar import ConsequencesParser
from itertools import chain


class StateMachine:
    def __init__(self):
        self._activeStates = set([])

    def addActiveState(self, n):
        self._activeStates.add(n)

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
        self._activeStates.update(trcs[0].n2 for trcs in transitionGen2)

        Property.properties.update(chain(*(trcs[1][0] for trcs in transitionGen2)))
        Property.properties.difference_update(chain(*(trcs[1][1] for trcs in transitionGen2)))

        Event.events.clear()
        Event.events.update(chain(*(trcs[1][2] for trcs in transitionGen2)))


class Node:
    def __init__(self, name):
        self.outputArcs = []
        self._name = name

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)


class Transition:
    def __init__(self, in1, in2, trigger, consequences):
        self.n1 = in1
        in1.outputArcs.append(self)
        self.n2 = in2
        self._trigger = trigger
        self._consequences = consequences

    def eval(self):
        for evaluation in self._trigger.eval():
            return evaluation

    def consequences(self, evaluation):
        consParsed = (ConsequencesParser.parse(cons) for cons in self._consequences)
        consEvaluated = [(add, cons.eval_update(evaluation)) for add, cons in consParsed]
        pToAdd = (cons for add, cons in consEvaluated if add and isinstance(cons, Property))
        pToRemove = (cons for add, cons in consEvaluated if not add and isinstance(cons, Property))
        eToAdd = (cons for add, cons in consEvaluated if add and isinstance(cons, Event))
        return pToAdd, pToRemove, eToAdd

    def __str__(self):
        return str(self.n1) + ' ' + str(self.n2)

    def __repr__(self):
        return str(self.n1) + ' ' + str(self.n2)


if __name__ == '__main__':
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)

    f1 = 'true'
    t1 = BExpression(BooleanExpressionParser.parse(f1))
    Transition(n1, n2, t1, ['A pW(0,0)', 'A pW(0,1)', 'A pW(0,2)'])

    f2 = 'pW(X,3)'
    t2 = BExpression(BooleanExpressionParser.parse(f2))
    Transition(n2, n3, t2, ['A pW(X,1)', 'R pW(X,3)'])

    f3 = 'pW(X,1)'
    t3 = BExpression(BooleanExpressionParser.parse(f3))
    Transition(n2, n2, t3, ['A pW(X,3)', 'R pW(X,1)'])

    f4 = 'pW(X,1)'
    t4 = BExpression(BooleanExpressionParser.parse(f3))
    Transition(n3, n2, t4, ['A pW(X,3)', 'R pW(X,1)'])

    sm = StateMachine()
    sm.addActiveState(n1)

    for i in xrange(10):
        print sm._activeStates, Property.properties, Event.events
        sm.tick()