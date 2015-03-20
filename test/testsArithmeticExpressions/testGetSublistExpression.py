from collections import deque

__author__ = 'mouton'

from arithmeticExpressions import ALitteral, ListLitteral, UndefinedLitteral, \
    SelfLitteral, LinkedListLitteral, SetLitteral, GetSublistExpression
from triggerExpressions import Evaluation
from database import Variable, UNDEFINED_PARAMETER
from unittest import TestCase


class TestGetSublistExpression(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

    def setUp(self):
        self.eval1 = Evaluation()
        self.eval2 = Evaluation()
        self.eval2[Variable('X')] = 2
        self.eval2[Variable('X2')] = 4
        self.eval2[Variable('T')] = 'abc'
        self.eval2[Variable('Z')] = 12.0

    def test_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [12.0, 'abc'])

    def test_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [12.0, 'abc'])

    def test_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([12.0, 'abc']))

    def test_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([12.0, 'abc']))

    def test_big_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [12.0, 'abc', 12.0])

    def test_big_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [12.0, 'abc', 12.0])

    def test_big_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([12.0, 'abc', 12.0]))

    def test_big_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([12.0, 'abc', 12.0]))

    def test_big_index1_and_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(5)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [])

    def test_big_index1_and_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(5)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [])

    def test_big_index1_and_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(5)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([]))

    def test_big_index1_and_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(5)
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([]))

    def test_index1_bigger_than_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(3)
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [])

    def test_index1_bigger_than_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(3)
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [])

    def test_index1_bigger_than_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(3)
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([]))

    def test_index1_bigger_than_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(3)
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([]))

    def test_negative_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [12.0, 'abc'])

    def test_negative_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [12.0, 'abc'])

    def test_negative_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([12.0, 'abc']))

    def test_negative_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([12.0, 'abc']))

    def test_negative_index1_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [12.0, 'abc'])

    def test_negative_index1_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [12.0, 'abc'])

    def test_negative_index1_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([12.0, 'abc']))

    def test_negative_index1_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([12.0, 'abc']))

    def test_negative_index1_and_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [12.0, 'abc'])

    def test_negative_index1_and_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [12.0, 'abc'])

    def test_negative_index1_and_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([12.0, 'abc']))

    def test_negative_index1_and_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(-3)
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([12.0, 'abc']))

    def test_none_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [12.0, 'abc', 12.0])

    def test_none_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [12.0, 'abc', 12.0])

    def test_none_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([12.0, 'abc', 12.0]))

    def test_none_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([12.0, 'abc', 12.0]))

    def test_none_index1_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [1, 12.0])

    def test_none_index1_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [1, 12.0])

    def test_none_index1_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([1, 12.0]))

    def test_none_index1_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([1, 12.0]))

    def test_none_index1_and_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), [1, 12.0, 'abc', 12.0])

    def test_none_index1_and_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [1, 12.0, 'abc', 12.0])

    def test_none_index1_and_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval1), deque([1, 12.0, 'abc', 12.0]))

    def test_none_index1_and_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([1, 12.0, 'abc', 12.0]))

    def test_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval1)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 2)

    def test_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval2)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 2)

    def test_not_none_index1_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_not_none_index1_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_big_index2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval1)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 3)

    def test_big_index2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(6)
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval2)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 3)

    def test_index1_bigger_than_index2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(3)
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_index1_bigger_than_index2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(3)
        index2 = ALitteral(2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_negative_index2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval1)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 2)

    def test_negative_index2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(-1)
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval2)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 2)

    def test_undefined_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = UndefinedLitteral()
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = UndefinedLitteral()
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = UndefinedLitteral()
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = UndefinedLitteral()
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_index2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = UndefinedLitteral()
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_index2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = UndefinedLitteral()
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_index1_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = UndefinedLitteral()
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_index1_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = UndefinedLitteral()
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_index1_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = UndefinedLitteral()
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_index1_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = UndefinedLitteral()
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_undefined_index1_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = UndefinedLitteral()
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_undefined_index1_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = UndefinedLitteral()
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral('def')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral('def')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral('def')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral('def')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral('def')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral('def')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index1_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index1_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index1_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index1_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index1_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index1_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index1_and_index_2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = ALitteral('ghi')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index1_and_index_2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = ALitteral('ghi')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index1_and_index_2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = ALitteral('ghi')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index1_and_index_2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = ALitteral('ghi')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_string_index1_and_index_2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = ALitteral('ghi')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_string_index1_and_index_2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral('def')
        index2 = ALitteral('ghi')
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(1.3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(1.3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(1.3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(1.3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(1.3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(1.3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index1_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index1_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index1_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index1_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index1_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index1_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index1_and_index_2_static_list_get_sublist_with_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = ALitteral(3.2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index1_and_index_2_static_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = ALitteral(3.2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index1_and_index_2_static_linkedlist_get_sublist_with_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = ALitteral(3.2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index1_and_index_2_static_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = ALitteral(3.2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_float_index1_and_index_2_static_set_get_sublist_with_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = ALitteral(3.2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval1)

    def test_float_index1_and_index_2_static_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1.3)
        index2 = ALitteral(3.2)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_evaluated_variable_index2_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(Variable('X'))
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), [12.0])

    def test_evaluated_variable_index2_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(Variable('X'))
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque([12.0]))

    def test_evaluated_variable_index2_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(Variable('X'))
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval2)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 2)

    def test_evaluated_variable_index1_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('X'))
        index2 = ALitteral(4)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), ['abc', 12.0])

    def test_evaluated_variable_index1_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('X'))
        index2 = ALitteral(4)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque(['abc', 12.0]))

    def test_evaluated_variable_index1_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('X'))
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_evaluated_variable_index1_and_index2_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('X'))
        index2 = ALitteral(Variable('X2'))
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), ['abc', 12.0])

    def test_evaluated_variable_index1_and_index2_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('X'))
        index2 = ALitteral(Variable('X2'))
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2), deque(['abc', 12.0]))

    def test_evaluated_variable_index1_and_index2_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('X'))
        index2 = ALitteral(Variable('X2'))
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2)

    def test_unevaluated_variable_index2_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(Variable('Y'))
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_index2_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = ALitteral(Variable('Y'))
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_index2_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = ALitteral(Variable('Y'))
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_index1_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('Y'))
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_index1_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('Y'))
        index2 = ALitteral(3)
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_unevaluated_variable_index1_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(Variable('Y'))
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(ValueError):
            expr.value(self.eval2)

    def test_self_litteral_index2_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = SelfLitteral()
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2, 2), [12.0])

    def test_self_litteral_index2_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = ALitteral(1)
        index2 = SelfLitteral()
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2, 2), deque([12.0]))

    def test_self_litteral_index2_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = None
        index2 = SelfLitteral()
        expr = GetSublistExpression(l, index1, index2)
        value = expr.value(self.eval2, 2)
        self.assertLessEqual(value, set([1, 12.0, 'abc']))
        self.assertEqual(len(value), 2)

    def test_self_litteral_index1_list_get_sublist_with_non_empty_evaluation(self):
        l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = SelfLitteral()
        index2 = ALitteral(4)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2, 2), ['abc', 12.0])

    def test_self_litteral_index1_linkedlist_get_sublist_with_non_empty_evaluation(self):
        l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = SelfLitteral()
        index2 = ALitteral(4)
        expr = GetSublistExpression(l, index1, index2)
        self.assertEqual(expr.value(self.eval2, 2), deque(['abc', 12.0]))

    def test_self_litteral_index1_set_get_sublist_with_non_empty_evaluation(self):
        l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
        index1 = SelfLitteral()
        index2 = None
        expr = GetSublistExpression(l, index1, index2)
        with self.assertRaises(TypeError):
            expr.value(self.eval2, 2)