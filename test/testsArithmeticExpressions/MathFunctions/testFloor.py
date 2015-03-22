__author__ = 'mouton'

from triggerExpressions import Evaluation
from unittest import TestCase
from math import pi, sqrt, floor
from arithmeticExpressions import ALitteral, Func, UndefinedLitteral, SelfLitteral
from database import Variable


class TestFloor(TestCase):

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

    def test_integer_floor_with_empty_evaluation(self):
        a1 = ALitteral(1)
        floorr = Func(a1, floor)
        self.assertEqual(floorr.value(self.eval1), floor(1))

    def test_integer_floor_with_non_empty_evaluation(self):
        a1 = ALitteral(1)
        floorr = Func(a1, floor)
        self.assertEqual(floorr.value(self.eval2), floor(1))

    def test_float_floor_with_empty_evaluation(self):
        a1 = ALitteral(pi)
        floorr = Func(a1, floor)
        self.assertEqual(floorr.value(self.eval1), floor(pi))

    def test_float_floor_with_non_empty_evaluation(self):
        a1 = ALitteral(pi)
        floorr = Func(a1, floor)
        self.assertEqual(floorr.value(self.eval2), floor(pi))

    def test_string_floor_with_empty_evaluation(self):
        a1 = ALitteral('abc')
        floorr = Func(a1, floor)
        with self.assertRaises(TypeError):
            floorr.value(self.eval1)

    def test_string_floor_with_non_empty_evaluation(self):
        a1 = ALitteral('abc')
        floorr = Func(a1, floor)
        with self.assertRaises(TypeError):
            floorr.value(self.eval2)

    def test_undefined_floor_with_empty_evaluation(self):
        a1 = UndefinedLitteral()
        floorr = Func(a1, floor)
        with self.assertRaises(TypeError):
            floorr.value(self.eval1)

    def test_undefined_floor_with_non_empty_evaluation(self):
        a1 = UndefinedLitteral()
        floorr = Func(a1, floor)
        with self.assertRaises(TypeError):
            floorr.value(self.eval2)

    def test_evaluated_variable_floor(self):
        a1 = ALitteral(Variable('X'))
        floorr = Func(a1, floor)
        self.assertEqual(floorr.value(self.eval2), floor(pi))

    def test_unevaluated_variable_floor(self):
        a1 = ALitteral(Variable('Y'))
        floorr = Func(a1, floor)
        with self.assertRaises(ValueError):
            floorr.value(self.eval2)

    def test_self_litteral_floor_with_empty_evaluation(self):
        a1 = SelfLitteral()
        floorr = Func(a1, floor)
        self.assertEqual(floorr.value(self.eval1, pi), floor(pi))

    def test_self_litteral_floor_with_non_empty_evaluation(self):
        a1 = SelfLitteral()
        floorr = Func(a1, floor)
        self.assertEqual(floorr.value(self.eval2, pi), floor(pi))