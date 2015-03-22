__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt, sin
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable


class TestSin(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

    def setUp(self):
        self.eval1 = Evaluation()
        self.eval2 = Evaluation()
        self.eval2[Variable('X')] = pi
        self.eval2[Variable('T')] = 'abc'
        self.eval2[Variable('Z')] = 12.0

    def test_integer_sin_with_empty_evaluation(self):
        a1 = ALitteral(1)
        expr = Func(a1, sin)
        self.assertEqual(expr.value(self.eval1), sin(1))

    def test_integer_sin_with_non_empty_evaluation(self):
        a1 = ALitteral(1)
        expr = Func(a1, sin)
        self.assertEqual(expr.value(self.eval2), sin(1))

    def test_float_sin_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        expr = Func(a1, sin)
        self.assertEqual(expr.value(self.eval1), sin(pi))

    def test_float_sin_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        expr = Func(a1, sin)
        self.assertEqual(expr.value(self.eval2), sin(pi))

    def test_string_sin_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        expr = Func(a1, sin)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_sin_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        expr = Func(a1, sin)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_sin_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        expr = Func(a1, sin)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_sin_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        expr = Func(a1, sin)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_evaluated_variable_sin(self):
        a1 = ALitteral(Variable('X'))
        expr = Func(a1, sin)
        self.assertEqual(expr.value(self.eval2), sin(pi))

    def test_unevaluated_variable_sin(self):
        a1 = ALitteral(Variable('Y'))
        expr = Func(a1, sin)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_self_litteral_sin_with_empty_evaluation(self):
        a1 = SelfLitteral()
        expr = Func(a1, sin)
        self.assertEqual(expr.value(self.eval1, pi), sin(pi))

    def test_self_litteral_sin_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        expr = Func(a1, sin)
        self.assertEqual(expr.value(self.eval2, pi), sin(pi))