__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable
from utils.mathutils import sign


class TestSign(TestCase):

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

    def test_integer_sign_with_empty_evaluation(self):
        a1 = ALitteral(1)
        signr = Func(a1, sign)
        self.assertEqual(signr.value(self.eval1), sign(1))

    def test_integer_sign_with_non_empty_evaluation(self):
        a1 = ALitteral(1)
        signr = Func(a1, sign)
        self.assertEqual(signr.value(self.eval2), sign(1))

    def test_float_sign_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        signr = Func(a1, sign)
        self.assertEqual(signr.value(self.eval1), sign(pi))

    def test_float_sign_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        signr = Func(a1, sign)
        self.assertEqual(signr.value(self.eval2), sign(pi))

    def test_string_sign_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        signr = Func(a1, sign)
        with self.assertRaises(TypeError):
            signr.value(self.eval1)

    def test_string_sign_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        signr = Func(a1, sign)
        with self.assertRaises(TypeError):
            signr.value(self.eval2)

    def test_undefined_sign_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        signr = Func(a1, sign)
        with self.assertRaises(TypeError):
            signr.value(self.eval1)

    def test_undefined_sign_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        signr = Func(a1, sign)
        with self.assertRaises(TypeError):
            signr.value(self.eval2)

    def test_evaluated_variable_sign(self):
        a1 = ALitteral(Variable('X'))
        signr = Func(a1, sign)
        self.assertEqual(signr.value(self.eval2), sign(pi))

    def test_unevaluated_variable_sign(self):
        a1 = ALitteral(Variable('Y'))
        signr = Func(a1, sign)
        with self.assertRaises(ValueError):
            signr.value(self.eval2)

    def test_self_litteral_sign_with_empty_evaluation(self):
        a1 = SelfLitteral()
        signr = Func(a1, sign)
        self.assertEqual(signr.value(self.eval1, pi), sign(pi))

    def test_self_litteral_sign_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        signr = Func(a1, sign)
        self.assertEqual(signr.value(self.eval2, pi), sign(pi))