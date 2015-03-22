__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt, atanh
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable


class TestAtanh(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

    def setUp(self):
        self.eval1 = Evaluation()
        self.eval2 = Evaluation()
        self.eval2[Variable('X')] = 0.5
        self.eval2[Variable('T')] = 'abc'
        self.eval2[Variable('Z')] = 12.0

    def test_integer_atanh_with_empty_evaluation(self):
        a1 = ALitteral(0)
        expr = Func(a1, atanh)
        self.assertEqual(expr.value(self.eval1), atanh(0))

    def test_integer_atanh_with_non_empty_evaluation(self):
        a1 = ALitteral(0)
        expr = Func(a1, atanh)
        self.assertEqual(expr.value(self.eval2), atanh(0))

    def test_float_atanh_with_empty_evaluation(self):
        a1 = ALitteral(0.5)
        expr = Func(a1, atanh)
        self.assertEqual(expr.value(self.eval1), atanh(0.5))

    def test_float_atanh_with_non_empty_evaluation(self):
        a1 = ALitteral(0.5)
        expr = Func(a1, atanh)
        self.assertEqual(expr.value(self.eval2), atanh(0.5))

    def test_bad_integer_atanh_with_empty_evaluation(self):
        a1 = ALitteral(-2)
        expr = Func(a1, atanh)
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_bad_integer_atanh_with_non_empty_evaluation(self):
        a1 = ALitteral(2)
        expr = Func(a1, atanh)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_bad_float_atanh_with_empty_evaluation(self):
        a1 = ALitteral(1.5)
        expr = Func(a1, atanh)
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_bad_float_atanh_with_non_empty_evaluation(self):
        a1 = ALitteral(-1.5)
        expr = Func(a1, atanh)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_string_atanh_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        expr = Func(a1, atanh)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_atanh_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        expr = Func(a1, atanh)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_atanh_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        expr = Func(a1, atanh)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_atanh_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        expr = Func(a1, atanh)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_evaluated_variable_atanh(self):
        a1 = ALitteral(Variable('X'))
        expr = Func(a1, atanh)
        self.assertEqual(expr.value(self.eval2), atanh(0.5))

    def test_unevaluated_variable_atanh(self):
        a1 = ALitteral(Variable('Y'))
        expr = Func(a1, atanh)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_self_litteral_atanh_with_empty_evaluation(self):
        a1 = SelfLitteral()
        expr = Func(a1, atanh)
        self.assertEqual(expr.value(self.eval1, 0.5), atanh(0.5))

    def test_self_litteral_atanh_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        expr = Func(a1, atanh)
        self.assertEqual(expr.value(self.eval2, 0.5), atanh(0.5))