__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt, ceil
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable


class TestCeil(TestCase):

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

    def test_integer_ceil_with_empty_evaluation(self):
        a1 = ALitteral(1)
        ceilr = Func(a1, ceil)
        self.assertEqual(ceilr.value(self.eval1), ceil(1))

    def test_integer_ceil_with_non_empty_evaluation(self):
        a1 = ALitteral(1)
        ceilr = Func(a1, ceil)
        self.assertEqual(ceilr.value(self.eval2), ceil(1))

    def test_float_ceil_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        ceilr = Func(a1, ceil)
        self.assertEqual(ceilr.value(self.eval1), ceil(pi))

    def test_float_ceil_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        ceilr = Func(a1, ceil)
        self.assertEqual(ceilr.value(self.eval2), ceil(pi))

    def test_string_ceil_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        ceilr = Func(a1, ceil)
        with self.assertRaises(TypeError):
            ceilr.value(self.eval1)

    def test_string_ceil_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        ceilr = Func(a1, ceil)
        with self.assertRaises(TypeError):
            ceilr.value(self.eval2)

    def test_undefined_ceil_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        ceilr = Func(a1, ceil)
        with self.assertRaises(TypeError):
            ceilr.value(self.eval1)

    def test_undefined_ceil_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        ceilr = Func(a1, ceil)
        with self.assertRaises(TypeError):
            ceilr.value(self.eval2)

    def test_evaluated_variable_ceil(self):
        a1 = ALitteral(Variable('X'))
        ceilr = Func(a1, ceil)
        self.assertEqual(ceilr.value(self.eval2), ceil(pi))

    def test_unevaluated_variable_ceil(self):
        a1 = ALitteral(Variable('Y'))
        ceilr = Func(a1, ceil)
        with self.assertRaises(ValueError):
            ceilr.value(self.eval2)

    def test_self_litteral_ceil_with_empty_evaluation(self):
        a1 = SelfLitteral()
        ceilr = Func(a1, ceil)
        self.assertEqual(ceilr.value(self.eval1, pi), ceil(pi))

    def test_self_litteral_ceil_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        ceilr = Func(a1, ceil)
        self.assertEqual(ceilr.value(self.eval2, pi), ceil(pi))