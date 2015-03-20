__author__ = 'mouton'

from unittest import TestCase

from triggerExpressions import Not, BLitteral, Evaluation
from database import Variable
from test.testsTriggersExpressions import simpleTests


class TestNot(TestCase):

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

    def test_eval_true_with_empty_previous_evaluation(self):
        self.eval_true(self.eval1)

    def test_eval_true_with_non_empty_previous_evaluation(self):
        self.eval_true(self.eval2)

    def eval_true(self, previousEvaluation):
        lit = BLitteral(False)
        trig = Not(lit)
        token = None

        simpleTests.test_evaluation(self, trig, previousEvaluation, token, previousEvaluation)

    def test_eval_false_with_empty_previous_evaluation(self):
        self.eval_false(self.eval1)

    def test_eval_false_with_non_empty_previous_evaluation(self):
        self.eval_false(self.eval2)

    def eval_false(self, previousEvaluation):
        lit = BLitteral(True)
        trig = Not(lit)
        token = None

        simpleTests.test_evaluation(self, trig, previousEvaluation, token)