__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable


class TestAbs(TestCase):

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

    def test_integer_abs_with_empty_evaluation(self):
        a1 = ALitteral(1)
        absr = Func(a1, abs)
        self.assertEqual(absr.value(self.eval1), abs(1))

    def test_integer_abs_with_non_empty_evaluation(self):
        a1 = ALitteral(1)
        absr = Func(a1, abs)
        self.assertEqual(absr.value(self.eval2), abs(1))

    def test_float_abs_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        absr = Func(a1, abs)
        self.assertEqual(absr.value(self.eval1), abs(pi))

    def test_float_abs_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        absr = Func(a1, abs)
        self.assertEqual(absr.value(self.eval2), abs(pi))

    def test_string_abs_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        absr = Func(a1, abs)
        with self.assertRaises(TypeError):
            absr.value(self.eval1)

    def test_string_abs_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        absr = Func(a1, abs)
        with self.assertRaises(TypeError):
            absr.value(self.eval2)

    def test_undefined_abs_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        absr = Func(a1, abs)
        with self.assertRaises(TypeError):
            absr.value(self.eval1)

    def test_undefined_abs_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        absr = Func(a1, abs)
        with self.assertRaises(TypeError):
            absr.value(self.eval2)

    def test_evaluated_variable_abs(self):
        a1 = ALitteral(Variable('X'))
        absr = Func(a1, abs)
        self.assertEqual(absr.value(self.eval2), abs(pi))

    def test_unevaluated_variable_abs(self):
        a1 = ALitteral(Variable('Y'))
        absr = Func(a1, abs)
        with self.assertRaises(ValueError):
            absr.value(self.eval2)

    def test_self_litteral_abs_with_empty_evaluation(self):
        a1 = SelfLitteral()
        absr = Func(a1, abs)
        self.assertEqual(absr.value(self.eval1, pi), abs(pi))

    def test_self_litteral_abs_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        absr = Func(a1, abs)
        self.assertEqual(absr.value(self.eval2, pi), abs(pi))