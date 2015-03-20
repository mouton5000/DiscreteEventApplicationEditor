__author__ = 'mouton'

from unittest import TestCase

from triggerExpressions import Timer, Evaluation
from database import Variable
from stateMachine import Token
from test.testsTriggersExpressions import simpleTests
from arithmeticExpressions import ALitteral


class TestTimer(TestCase):
    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

    def setUp(self):
        self.eval1 = Evaluation()
        self.eval2 = Evaluation()
        self.eval2[Variable('X')] = 1
        self.eval2[Variable('Y')] = 'abc'
        self.eval2[Variable('Z')] = 12.0
        self.eval2[Variable('T')] = True

    def test_timer_when_token_did_not_wait_enough_with_empty_previous_evaluation(self):
        self.timer_when_token_did_not_wait_enough(self.eval1)

    def test_timer_when_token_did_not_wait_enough_with_none_empty_previous_evaluation(self):
        self.timer_when_token_did_not_wait_enough(self.eval2)

    def timer_when_token_did_not_wait_enough(self, previousEvaluation):
        trig = Timer(ALitteral(30))
        token = Token(None, [], {})

        for i in xrange(30):
            simpleTests.test_evaluation(self, trig, previousEvaluation, token)
            token.oneMoreFrame()

    def test_timer_when_token_waited_enough_with_empty_previous_evaluation(self):
        self.timer_when_token_waited_enough(self.eval1)

    def test_timer_when_token_waited_enough_with_none_empty_previous_evaluation(self):
        self.timer_when_token_waited_enough(self.eval2)

    def timer_when_token_waited_enough(self, previousEvaluation):
        trig = Timer(ALitteral(30))
        token = Token(None, [], {})

        for i in xrange(30):
            token.oneMoreFrame()

        for i in xrange(30):
            token.oneMoreFrame()
            simpleTests.test_evaluation(self, trig, previousEvaluation, token, previousEvaluation)