__author__ = 'mouton'

from unittest import TestCase

from triggerExpressions import Or, BLitteral, Evaluation
from database import Variable
from test.testsTriggersExpressions import simpleTests


class TestOr(TestCase):

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

    def test_eval_true_true_with_empty_previous_evaluation(self):
        self.eval_true_true(self.eval1)

    def test_eval_true_true_with_non_empty_previous_evaluation(self):
        self.eval_true_true(self.eval2)

    def eval_true_true(self, previousEvaluation):
        lit1 = BLitteral(True)
        lit2 = BLitteral(True)
        token = None
        trig = Or(lit1, lit2)

        simpleTests.test_evaluation(self, trig, previousEvaluation, token, previousEvaluation, previousEvaluation)

    def test_eval_true_false_with_empty_previous_evaluation(self):
        self.eval_true(self.eval1, True, False)

    def test_eval_true_false_with_non_empty_previous_evaluation(self):
        self.eval_true(self.eval2, True, False)

    def test_eval_false_true_with_empty_previous_evaluation(self):
        self.eval_true(self.eval1, False, True)

    def test_eval_false_true_with_non_empty_previous_evaluation(self):
        self.eval_true(self.eval2, False, True)

    def eval_true(self, previousEvaluation, b1, b2):
        lit1 = BLitteral(b1)
        lit2 = BLitteral(b2)
        token = None
        trig = Or(lit1, lit2)

        simpleTests.test_evaluation(self, trig, previousEvaluation, token, previousEvaluation)

    def test_eval_false_false_with_empty_previous_evaluation(self):
        self.eval_false(self.eval1)

    def test_eval_false_false_with_non_empty_previous_evaluation(self):
        self.eval_false(self.eval2)

    def eval_false(self, previousEvaluation):
        lit1 = BLitteral(False)
        lit2 = BLitteral(False)
        token = None
        trig = Or(lit1, lit2)

        simpleTests.test_evaluation(self, trig, previousEvaluation, token)