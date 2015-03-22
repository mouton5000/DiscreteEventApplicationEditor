__author__ = 'mouton'

from unittest import TestCase

from triggerExpressions import Evaluation, LeqThan
from arithmeticExpressions import ALitteral, UndefinedLitteral, Division
from database import Variable
from test.testsTriggersExpressions import simpleTests
from math import pi, sqrt


class TestLowerOrEqualsThan(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

    def setUp(self):
        self.eval1 = Evaluation()
        self.eval2 = Evaluation()
        self.eval2[Variable('X')] = 1
        self.eval2[Variable('T')] = 'abc'
        self.eval2[Variable('Z')] = 12.0

    def test_eval_true_not_same_integer_integer_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1)
        expr2 = ALitteral(2)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_not_same_float_float_with_empty_previous_evaluation(self):
        expr1 = ALitteral(sqrt(2))
        expr2 = ALitteral(pi)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_not_same_string_string_with_empty_previous_evaluation(self):
        expr1 = ALitteral('abc')
        expr2 = ALitteral('def')
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_not_same_integer_float_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1)
        expr2 = ALitteral(2.0)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_not_same_float_integer_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1.0)
        expr2 = ALitteral(2)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_not_same_integer_string_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1)
        expr2 = ALitteral('abc')
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_not_same_float_string_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1.0)
        expr2 = ALitteral('abc')
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_same_integer_integer_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1)
        expr2 = ALitteral(1)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_same_integer_float_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1)
        expr2 = ALitteral(1.0)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_same_float_integer_with_empty_previous_evaluation(self):
        expr1 = ALitteral(1.0)
        expr2 = ALitteral(1)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_same_float_float_with_empty_previous_evaluation(self):
        expr1 = ALitteral(pi)
        expr2 = ALitteral(pi)
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_true_same_string_string_with_empty_previous_evaluation(self):
        expr1 = ALitteral('abc')
        expr2 = ALitteral('abc')
        self.eval_lower_or_equals_than(self.eval1, expr1, expr2)

    def eval_lower_or_equals_than(self, previousEvaluation, expr1, expr2):
        token = None
        trig = LeqThan(expr1, expr2)

        simpleTests.test_evaluation(self, trig, previousEvaluation, token, previousEvaluation)

    def test_eval_false_not_same_integer_integer_with_empty_previous_evaluation(self):
        expr1 = ALitteral(2)
        expr2 = ALitteral(1)
        self.eval_not_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_false_not_same_float_float_with_empty_previous_evaluation(self):
        expr1 = ALitteral(pi)
        expr2 = ALitteral(sqrt(2))
        self.eval_not_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_false_not_same_string_string_with_empty_previous_evaluation(self):
        expr1 = ALitteral('def')
        expr2 = ALitteral('abc')
        self.eval_not_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_false_not_same_float_integer_with_empty_previous_evaluation(self):
        expr1 = ALitteral(2)
        expr2 = ALitteral(1.0)
        self.eval_not_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_false_not_same_integer_float_with_empty_previous_evaluation(self):
        expr1 = ALitteral(2.0)
        expr2 = ALitteral(1)
        self.eval_not_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_false_not_same_integer_string_with_empty_previous_evaluation(self):
        expr1 = ALitteral('abc')
        expr2 = ALitteral(1)
        self.eval_not_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_false_not_same_float_string_with_empty_previous_evaluation(self):
        expr1 = ALitteral('abc')
        expr2 = ALitteral(1.0)
        self.eval_not_lower_or_equals_than(self.eval1, expr1, expr2)

    def test_eval_ValueError_integer(self):
        expr1 = ALitteral(Variable('Y'))
        expr2 = ALitteral(1)
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_ValueError_float(self):
        expr1 = ALitteral(Variable('Y'))
        expr2 = ALitteral(12.0)
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_ValueError_string(self):
        expr1 = ALitteral(Variable('Y'))
        expr2 = ALitteral('abc')
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_integer_ValueError(self):
        expr1 = ALitteral(1)
        expr2 = ALitteral(Variable('Y'))
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_float_ValueError(self):
        expr1 = ALitteral(12.0)
        expr2 = ALitteral(Variable('Y'))
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_string_ValueError(self):
        expr1 = ALitteral('abc')
        expr2 = ALitteral(Variable('Y'))
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_TypeError_integer(self):
        expr1 = UndefinedLitteral()
        expr2 = ALitteral(1)
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_TypeError_float(self):
        expr1 = UndefinedLitteral()
        expr2 = ALitteral(12.0)
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_TypeError_string(self):
        expr1 = UndefinedLitteral()
        expr2 = ALitteral('abc')
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_integer_TypeError(self):
        expr1 = ALitteral(1)
        expr2 = UndefinedLitteral()
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_float_TypeError(self):
        expr1 = ALitteral(12.0)
        expr2 = UndefinedLitteral()
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_string_TypeError(self):
        expr1 = ALitteral('abc')
        expr2 = UndefinedLitteral()
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_ArithmeticError_integer(self):
        expr1 = Division(ALitteral(1), ALitteral(0))
        expr2 = ALitteral(1)
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_ArithmeticError_float(self):
        expr1 = Division(ALitteral(1), ALitteral(0))
        expr2 = ALitteral(12.0)
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_ArithmeticError_string(self):
        expr1 = Division(ALitteral(1), ALitteral(0))
        expr2 = ALitteral('abc')
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_integer_ArithmeticError(self):
        expr1 = ALitteral(1)
        expr2 = Division(ALitteral(1), ALitteral(0))
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_float_ArithmeticError(self):
        expr1 = ALitteral(12.0)
        expr2 = Division(ALitteral(1), ALitteral(0))
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def test_eval_string_ArithmeticError(self):
        expr1 = ALitteral('abc')
        expr2 = Division(ALitteral(1), ALitteral(0))
        self.eval_not_lower_or_equals_than(self.eval2, expr1, expr2)

    def eval_not_lower_or_equals_than(self, previousEvaluation, expr1, expr2):
        token = None
        trig = LeqThan(expr1, expr2)

        simpleTests.test_evaluation(self, trig, previousEvaluation, token)