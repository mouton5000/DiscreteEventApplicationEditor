__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt
from arithmeticExpressions import ALitteral, Division, UndefinedLitteral, SelfLitteral
from database import Variable


class TestDivision(TestCase):

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

    def test_integers_division_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1), 0.5)

    def test_integers_division_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), 0.5)

    def test_bad_integer_division_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(0)
        expr = Division(a1, a2)
        with self.assertRaises(ArithmeticError):
            expr.value(self.eval1)

    def test_bad_integer_division_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(0)
        expr = Division(a1, a2)
        with self.assertRaises(ArithmeticError):
            expr.value(self.eval2)

    def test_strings_division_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_strings_division_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_floats_division_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1), pi / sqrt(2))

    def test_floats_division_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), pi / sqrt(2))

    def test_bad_float_division_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(0.0)
        expr = Division(a1, a2)
        with self.assertRaises(ArithmeticError):
            expr.value(self.eval1)

    def test_bad_float_division_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(0.0)
        expr = Division(a1, a2)
        with self.assertRaises(ArithmeticError):
            expr.value(self.eval2)

    def test_integer_string_division_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_integer_string_division_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_string_integer_division_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_string_integer_division_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_integer_float_division_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1), 10 / sqrt(2))

    def test_integer_float_division_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), 10 / sqrt(2))

    def test_float_integer_division_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1), pi / 20)

    def test_float_integer_division_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), pi / 20)

    def test_string_float_division_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_string_float_division_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_float_string_division_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval1)

    def test_float_string_division_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_integer_undefined_division_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_integer_undefined_division_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_integer_division_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_integer_division_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_undefined_division_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_undefined_division_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_string_division_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_string_division_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_undefined_division_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_undefined_division_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_float_division_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_float_division_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_undefined_division_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_undefined_division_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_integer_evaluated_variable_division(self):
        a1 = ALitteral(10)
        a2 = ALitteral(Variable('X'))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), 10)

    def test_evaluated_variable_integer_division(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), 1.0/20)

    def test_string_evaluated_variable_division(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(Variable('X'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_evaluated_variable_string_division(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_float_evaluated_variable_division(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(Variable('X'))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), pi)

    def test_evaluated_variable_float_division(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), 1 / sqrt(2))

    def test_evaluated_variable_evaluated_variable_division(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(Variable('X'))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2), 1)

    def test_evaluated_variable_undefined_division(self):
        a1 = ALitteral(Variable('X'))
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2), 0

    def test_undefined_evaluated_variable_division(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(Variable('X'))
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2), 0

    def test_integer_unevaluated_variable_division(self):
        a1 = ALitteral(10)
        a2 = ALitteral(Variable('Y'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_integer_division(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_string_unevaluated_variable_division(self):
        a1 = ALitteral('abc')
        a2 = ALitteral(Variable('Y'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_string_division(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_float_unevaluated_variable_division(self):
        a1 = ALitteral(pi)
        a2 = ALitteral(Variable('Y'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_float_division(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_unevaluated_variable_division(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(Variable('Y'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_evaluated_variable_division(self):
        a1 = ALitteral(Variable('Y'))
        a2 = ALitteral(Variable('X'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_evaluated_variable_unevaluated_variable_division(self):
        a1 = ALitteral(Variable('X'))
        a2 = ALitteral(Variable('Y'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_undefined_division(self):
        a1 = ALitteral(Variable('Y'))
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2), 0

    def test_undefined_unevaluated_variable_division(self):
        a1 = UndefinedLitteral()
        a2 = ALitteral(Variable('Y'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_integer_self_litteral_division_with_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 10)

    def test_integer_self_litteral_division_with_non_empty_evaluation(self):
        a1 = ALitteral(10)
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 10)

    def test_self_litteral_integer_division_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 1.0 / 20.0)

    def test_self_litteral_integer_division_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(20)
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 1.0 / 20.0)

    def test_string_self_litteral_division_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval1, 1)

    def test_string_self_litteral_division_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2, 1)

    def test_self_litteral_string_division_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval1, 1)

    def test_self_litteral_string_division_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral('def')
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2, 1)

    def test_float_self_litteral_division_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), pi)

    def test_float_self_litteral_division_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), pi)

    def test_self_litteral_float_division_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 1 / sqrt(2))

    def test_self_litteral_float_division_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = ALitteral(sqrt(2))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 1 / sqrt(2))

    def test_self_litteral_self_litteral_division_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval1, 1), 1)

    def test_self_litteral_self_litteral_division_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2, 1), 1)

    def test_self_litteral_undefined_division_with_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1, 1)

    def test_self_litteral_undefined_division_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        a2 = UndefinedLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2, 1)

    def test_undefined_self_litteral_division_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1, 1)

    def test_undefined_self_litteral_division_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2, 1)

    def test_self_litteral_evaluated_variable_division(self):
        a1 = ALitteral(Variable('X'))
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2, 2), 0.5)

    def test_evaluated_variable_self_litteral_division(self):
        a1 = SelfLitteral()
        a2 = ALitteral(Variable('X'))
        expr = Division(a1, a2)
        self.assertEqual(expr.value(self.eval2, 2), 2)

    def test_self_litteral_unevaluated_variable_division(self):
        a1 = SelfLitteral()
        a2 = ALitteral(Variable('Y'))
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2, 1)

    def test_unevaluated_variable_self_litteral_division(self):
        a1 = ALitteral(Variable('Y'))
        a2 = SelfLitteral()
        expr = Division(a1, a2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2, 1)