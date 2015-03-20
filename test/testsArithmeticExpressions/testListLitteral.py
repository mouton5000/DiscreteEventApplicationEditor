__author__ = 'mouton'

from arithmeticExpressions import ALitteral, ListLitteral, UndefinedLitteral, SelfLitteral
from triggerExpressions import Evaluation
from database import Variable, UNDEFINED_PARAMETER
from unittest import TestCase


class TestListLitteral(TestCase):

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

    def test_empty_list_with_empty_evaluation(self):
        expr = ListLitteral([])
        self.assertEqual(expr.value(self.eval1), [])

    def test_empty_list_with_non_empty_evaluation(self):
        expr = ListLitteral([])
        self.assertEqual(expr.value(self.eval2), [])

    def test_static_list_with_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        self.assertEqual(expr.value(self.eval1), [1, 12.0, 'abc', 12.0])

    def test_static_list_with_non_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        self.assertEqual(expr.value(self.eval2), [1, 12.0, 'abc', 12.0])

    def test_undefined_list_with_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(12.0), UndefinedLitteral(),
                             ALitteral('abc'), UndefinedLitteral()])
        self.assertEqual(expr.value(self.eval1), [1, 12.0, UNDEFINED_PARAMETER, 'abc', UNDEFINED_PARAMETER])

    def test_undefined_list_with_non_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(12.0), UndefinedLitteral(),
                             ALitteral('abc'), UndefinedLitteral()])
        self.assertEqual(expr.value(self.eval2), [1, 12.0, UNDEFINED_PARAMETER, 'abc', UNDEFINED_PARAMETER])

    def test_evaluated_variable_list_with_non_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(Variable('X')), ALitteral(Variable('X')), ALitteral(12.0)])
        self.assertEqual(expr.value(self.eval2), [1, 1, 1, 12.0])

    def test_unevaluated_variable_list_with_non_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(Variable('Y')), ALitteral(Variable('X')), ALitteral(12.0)])
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_self_litteral_list_with_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(12.0), SelfLitteral(),
                             ALitteral('abc'), SelfLitteral()])
        self.assertEqual(expr.value(self.eval1, 'def'), [1, 12.0, 'def', 'abc', 'def'])

    def test_self_litteral_list_with_non_empty_evaluation(self):
        expr = ListLitteral([ALitteral(1), ALitteral(12.0), SelfLitteral(),
                             ALitteral('abc'), SelfLitteral()])
        self.assertEqual(expr.value(self.eval2, 'def'), [1, 12.0, 'def', 'abc', 'def'])