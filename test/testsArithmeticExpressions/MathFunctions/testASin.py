__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt, asin
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable


class TestAsin(TestCase):

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

    def test_integer_asin_with_empty_evaluation(self):
        a1 = ALitteral(1)
        expr = Func(a1, asin)
        self.assertEqual(expr.value(self.eval1), asin(1))

    def test_integer_asin_with_non_empty_evaluation(self):
        a1 = ALitteral(1)
        expr = Func(a1, asin)
        self.assertEqual(expr.value(self.eval2), asin(1))

    def test_float_asin_with_empty_evaluation(self):
        a1 = ALitteral(0.5)
        expr = Func(a1, asin)
        self.assertEqual(expr.value(self.eval1), asin(0.5))

    def test_float_asin_with_non_empty_evaluation(self):
        a1 = ALitteral(0.5)
        expr = Func(a1, asin)
        self.assertEqual(expr.value(self.eval2), asin(0.5))

    def test_bad_integer_log_with_empty_evaluation(self):
        a1 = ALitteral(-2)
        logr = Func(a1, asin)
        with self.assertRaises(ValueError):
            logr.value(self.eval1)

    def test_bad_integer_log_with_non_empty_evaluation(self):
        a1 = ALitteral(2)
        logr = Func(a1, asin)
        with self.assertRaises(ValueError):
            logr.value(self.eval2)

    def test_bad_float_log_with_empty_evaluation(self):
        a1 = ALitteral(-2.2)
        logr = Func(a1, asin)
        with self.assertRaises(ValueError):
            logr.value(self.eval1)

    def test_bad_float_log_with_non_empty_evaluation(self):
        a1 = ALitteral(2.2)
        logr = Func(a1, asin)
        with self.assertRaises(ValueError):
            logr.value(self.eval2)


    def test_string_asin_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        expr = Func(a1, asin)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_asin_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        expr = Func(a1, asin)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_asin_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        expr = Func(a1, asin)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_asin_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        expr = Func(a1, asin)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_evaluated_variable_asin(self):
        a1 = ALitteral(Variable('X'))
        expr = Func(a1, asin)
        self.assertEqual(expr.value(self.eval2), asin(0.5))

    def test_unevaluated_variable_asin(self):
        a1 = ALitteral(Variable('Y'))
        expr = Func(a1, asin)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_self_litteral_asin_with_empty_evaluation(self):
        a1 = SelfLitteral()
        expr = Func(a1, asin)
        self.assertEqual(expr.value(self.eval1, 0.5), asin(0.5))

    def test_self_litteral_asin_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        expr = Func(a1, asin)
        self.assertEqual(expr.value(self.eval2, 0.5), asin(0.5))