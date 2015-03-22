__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt, log
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable


class TestLog(TestCase):

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

    def test_integer_log_with_empty_evaluation(self):
        a1 = ALitteral(1)
        logr = Func(a1, log)
        self.assertEqual(logr.value(self.eval1), log(1))

    def test_integer_log_with_non_empty_evaluation(self):
        a1 = ALitteral(1)
        logr = Func(a1, log)
        self.assertEqual(logr.value(self.eval2), log(1))

    def test_float_log_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        logr = Func(a1, log)
        self.assertEqual(logr.value(self.eval1), log(pi))

    def test_float_log_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        logr = Func(a1, log)
        self.assertEqual(logr.value(self.eval2), log(pi))

    def test_bad_integer_log_with_empty_evaluation(self):
        a1 = ALitteral(-1)
        logr = Func(a1, log)
        with self.assertRaises(ValueError):
            logr.value(self.eval1)

    def test_bad_integer_log_with_non_empty_evaluation(self):
        a1 = ALitteral(-1)
        logr = Func(a1, log)
        with self.assertRaises(ValueError):
            logr.value(self.eval2)

    def test_bad_float_log_with_empty_evaluation(self):
        a1 = ALitteral(-pi)
        logr = Func(a1, log)
        with self.assertRaises(ValueError):
            logr.value(self.eval1)

    def test_bad_float_log_with_non_empty_evaluation(self):
        a1 = ALitteral(-pi)
        logr = Func(a1, log)
        with self.assertRaises(ValueError):
            logr.value(self.eval2)

    def test_string_log_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        logr = Func(a1, log)
        with self.assertRaises(TypeError):
            logr.value(self.eval1)

    def test_string_log_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        logr = Func(a1, log)
        with self.assertRaises(TypeError):
            logr.value(self.eval2)

    def test_undefined_log_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        logr = Func(a1, log)
        with self.assertRaises(TypeError):
            logr.value(self.eval1)

    def test_undefined_log_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        logr = Func(a1, log)
        with self.assertRaises(TypeError):
            logr.value(self.eval2)

    def test_evaluated_variable_log(self):
        a1 = ALitteral(Variable('X'))
        logr = Func(a1, log)
        self.assertEqual(logr.value(self.eval2), log(pi))

    def test_unevaluated_variable_log(self):
        a1 = ALitteral(Variable('Y'))
        logr = Func(a1, log)
        with self.assertRaises(ValueError):
            logr.value(self.eval2)

    def test_self_litteral_log_with_empty_evaluation(self):
        a1 = SelfLitteral()
        logr = Func(a1, log)
        self.assertEqual(logr.value(self.eval1, pi), log(pi))

    def test_self_litteral_log_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        logr = Func(a1, log)
        self.assertEqual(logr.value(self.eval2, pi), log(pi))