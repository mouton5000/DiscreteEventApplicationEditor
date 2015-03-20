__author__ = 'mouton'

from arithmeticExpressions import ALitteral
from triggerExpressions import Evaluation
from database import Variable
from unittest import TestCase


class TestALitteral(TestCase):

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

    def test_integer_value_with_empty_evaluation(self):
        for i in xrange(100):
            expr = ALitteral(i)
            self.assertEqual(expr.value(self.eval1), i)

    def test_integer_value_with_non_empty_evaluation(self):
        for i in xrange(100):
            expr = ALitteral(i)
            self.assertEqual(expr.value(self.eval2), i)

    def test_string_value_with_empty_evaluation(self):
        for i in ['abc', '', '-12']:
            expr = ALitteral(i)
            self.assertEqual(expr.value(self.eval1), i)

    def test_string_value_with_non_empty_evaluation(self):
        for i in ['abc', '', '-12']:
            expr = ALitteral(i)
            self.assertEqual(expr.value(self.eval2), i)

    def test_float_value_with_empty_evaluation(self):
        from math import pi, e, sqrt
        for i in [1.0, 0.0, 3.14, sqrt(2), pi, e]:
            expr = ALitteral(i)
            self.assertEqual(expr.value(self.eval1), i)

    def test_float_value_with_non_empty_evaluation(self):
        from math import pi, e, sqrt
        for i in [1.0, 0.0, 3.14, sqrt(2), pi, e]:
            expr = ALitteral(i)
            self.assertEqual(expr.value(self.eval2), i)

    def test_fail_variable_value_with_empty_evaluation(self):
        expr = ALitteral(Variable('X'))
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_success_variable_value_with_non_empty_evaluation(self):
        expr = ALitteral(Variable('X'))
        self.assertEqual(expr.value(self.eval2), 1)
        expr = ALitteral(Variable('Y'))
        self.assertEqual(expr.value(self.eval2), 'abc')
        expr = ALitteral(Variable('Z'))
        self.assertEqual(expr.value(self.eval2), 12.0)

    def test_fail_variable_value_with_non_empty_evaluation(self):
        expr = ALitteral(Variable('T'))
        with self.assertRaises(ValueError):
            expr.value(self.eval2)