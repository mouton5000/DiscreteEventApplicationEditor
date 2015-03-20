__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt
from arithmeticExpressions import ALitteral, Addition, UndefinedLitteral, SelfLitteral
from database import Variable


class TestAddition(TestCase):

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

    def test_integers_addition_with_non_empty_evaluation_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), 30)

    def test_integers_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 30)

    def test_strings_addition_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), 'abcdef')

    def test_strings_addition_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 'abcdef')

    def test_floats_addition_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), pi + sqrt(2))

    def test_floats_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), pi + sqrt(2))

    def test_integer_string_addition_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), '10def')

    def test_integer_string_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), '10def')

    def test_string_integer_addition_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), 'abc20')

    def test_string_integer_addition_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 'abc20')

    def test_integer_float_addition_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), 10 + sqrt(2))

    def test_integer_float_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 10 + sqrt(2))

    def test_float_integer_addition_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), pi + 20)

    def test_float_integer_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), pi + 20)

    def test_string_float_addition_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), 'abc' + str(sqrt(2)))

    def test_string_float_addition_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 'abc' + str(sqrt(2)))

    def test_float_string_addition_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1), str(pi) + 'def')

    def test_float_string_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), str(pi) + 'def')

    def test_integer_undefined_addition_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_integer_undefined_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_integer_addition_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_integer_addition_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_undefined_addition_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_undefined_addition_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_string_addition_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_string_addition_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_undefined_addition_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_undefined_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_float_addition_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_float_addition_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_undefined_addition_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_undefined_addition_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_integer_evaluated_variable_addition(self):
        a1 = ALitteral(10)
        a2 = ALitteral(Variable('X'))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 11)

    def test_evaluated_variable_integer_addition(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 21)

    def test_string_evaluated_variable_addition(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(Variable('X'))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 'abc1')

    def test_evaluated_variable_string_addition(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), '1def')

    def test_float_evaluated_variable_addition(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(Variable('X'))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), pi + 1)

    def test_evaluated_variable_float_addition(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 1 + sqrt(2))

    def test_evaluated_variable_evaluated_variable_addition(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(Variable('X'))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2), 2)

    def test_evaluated_variable_undefined_addition(self):
        a1 = ALitteral(Variable('X'))
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2), 0

    def test_undefined_evaluated_variable_addition(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(Variable('X'))
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2), 0

    def test_integer_unevaluated_variable_addition(self):
        a1 = ALitteral(10)
        a2 = ALitteral(Variable('Y'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_integer_addition(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_string_unevaluated_variable_addition(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(Variable('Y'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_string_addition(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_float_unevaluated_variable_addition(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(Variable('Y'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_float_addition(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_unevaluated_variable_addition(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(Variable('Y'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_evaluated_variable_addition(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(Variable('X'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_evaluated_variable_unevaluated_variable_addition(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(Variable('Y'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_undefined_addition(self):
        a1 = ALitteral(Variable('Y'))
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_undefined_unevaluated_variable_addition(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(Variable('Y'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2),

    def test_integer_self_litteral_addition_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 11)

    def test_integer_self_litteral_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 11)

    def test_self_litteral_integer_addition_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 21)

    def test_self_litteral_integer_addition_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(20)
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 21)

    def test_string_self_litteral_addition_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 'abc1')

    def test_string_self_litteral_addition_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 'abc1')

    def test_self_litteral_string_addition_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), '1def')

    def test_self_litteral_string_addition_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral('def')
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), '1def')

    def test_float_self_litteral_addition_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), pi + 1)

    def test_float_self_litteral_addition_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), pi + 1)

    def test_self_litteral_float_addition_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 1 + sqrt(2))

    def test_self_litteral_float_addition_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 1 + sqrt(2))

    def test_self_litteral_self_litteral_addition_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 2)

    def test_self_litteral_self_litteral_addition_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 2)

    def test_self_litteral_undefined_addition_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1, 1)

    def test_self_litteral_undefined_addition_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = UndefinedLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2, 1)

    def test_undefined_self_litteral_addition_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1, 1)

    def test_undefined_self_litteral_addition_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2, 1)

    def test_self_litteral_evaluated_variable_addition(self):
        a1 = ALitteral(Variable('X'))
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 2)

    def test_evaluated_variable_self_litteral_addition(self):
        a1 = SelfLitteral()
        a2 = ALitteral(Variable('X'))
        expr = Addition(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 2)

    def test_self_litteral_unevaluated_variable_addition(self):
        a1 = SelfLitteral()
        a2 = ALitteral(Variable('Y'))
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2, 1)

    def test_unevaluated_variable_self_litteral_addition(self):
        a1 = ALitteral(Variable('Y'))
        a2 = SelfLitteral()
        expr = Addition(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2, 1)
