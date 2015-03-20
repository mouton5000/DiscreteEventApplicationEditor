__author__ = 'mouton'

from arithmeticExpressions import UndefinedLitteral
from triggerExpressions import Evaluation
from database import Variable, UNDEFINED_PARAMETER
from unittest import TestCase


class TestUndefinnedLitteral(TestCase):

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

    def test_with_empty_evaluation(self):
        expr = UndefinedLitteral()
        self.assertEqual(expr.value(self.eval1), UNDEFINED_PARAMETER)

    def test_with_non_empty_evaluation(self):
        expr = UndefinedLitteral()
        self.assertEqual(expr.value(self.eval2), UNDEFINED_PARAMETER)