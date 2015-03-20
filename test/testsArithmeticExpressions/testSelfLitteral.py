__author__ = 'mouton'

from arithmeticExpressions import SelfLitteral
from triggerExpressions import Evaluation
from database import Variable
from unittest import TestCase


class TestSelfLitteral(TestCase):

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

    def test_not_none_self_litteral_with_empty_evaluation(self):
        expr = SelfLitteral()
        self.assertEquals(expr.value(self.eval1, 10), 10)

    def test_not_none_self_litteral_with_non_empty_evaluation(self):
        expr = SelfLitteral()
        self.assertEquals(expr.value(self.eval2, 10), 10)

    def test_none_self_litteral_with_empty_evaluation(self):
        expr = SelfLitteral()
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_none_self_litteral_with_non_empty_evaluation(self):
        expr = SelfLitteral()
        with self.assertRaises(ValueError):
            expr.value(self.eval2)