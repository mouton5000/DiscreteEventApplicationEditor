# __author__ = 'mouton'
#
# from arithmeticExpressions import ALitteral, ListLitteral, UndefinedLitteral, \
#     SelfLitteral, LinkedListLitteral, SetLitteral, GetItemExpression
# from triggerExpressions import Evaluation
# from database import Variable, UNDEFINED_PARAMETER
# from unittest import TestCase
#
#
# class TestGetItemExpression(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         import grammar.grammars
#         grammar.grammars.compileGrammars()
#
#     def setUp(self):
#         self.eval1 = Evaluation()
#         self.eval2 = Evaluation()
#         self.eval2[Variable('X')] = 0
#         self.eval2[Variable('T')] = 'abc'
#         self.eval2[Variable('Z')] = 12.0
#
#     def test_static_list_get_item_with_empty_evaluation(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval1), 12.0)
#
#     def test_static_list_get_item_with_non_empty_evaluation(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2), 12.0)
#
#     def test_static_linkedlist_get_item_with_empty_evaluation(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval1), 12.0)
#
#     def test_static_linkedlist_get_item_with_non_empty_evaluation(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2), 12.0)
#
#     def test_static_set_get_item_with_empty_evaluation(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2)
#
#     def test_static_set_get_item_with_non_empty_evaluation(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2)
#
#     def test_negative_index_static_list_get_item_with_empty_evaluation(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(-2)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval1), 'abc')
#
#     def test_negative_index_static_list_get_item_with_non_empty_evaluation(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(-2)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2), 'abc')
#
#     def test_negative_index_static_linkedlist_get_item_with_empty_evaluation(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(-2)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval1), 'abc')
#
#     def test_negative_index_static_linkedlist_get_item_with_non_empty_evaluation(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(-2)
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2), 'abc')
#
#     def test_negative_index_static_set_get_item_with_empty_evaluation(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(-1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2)
#
#     def test_negative_index_static_set_get_item_with_non_empty_evaluation(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(-1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2)
#
#     def test_empty_list_get_item_with_empty_evaluation(self):
#         l = ListLitteral([])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(IndexError):
#             expr.value(self.eval1)
#
#     def test_empty_list_get_item_with_non_empty_evaluation(self):
#         l = ListLitteral([])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(IndexError):
#             expr.value(self.eval2)
#
#     def test_empty_linkedlist_get_item_with_empty_evaluation(self):
#         l = LinkedListLitteral([])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(IndexError):
#             expr.value(self.eval1)
#
#     def test_empty_linedlist_get_item_with_non_empty_evaluation(self):
#         l = LinkedListLitteral([])
#         index = ALitteral(1)
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(IndexError):
#             expr.value(self.eval2)
#
#     def test_empty_set_get_item_with_empty_evaluation(self):
#         l = SetLitteral([])
#         index = UndefinedLitteral()
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(StopIteration):
#             expr.value(self.eval1)
#
#     def test_empty_set_get_item_with_non_empty_evaluation(self):
#         l = SetLitteral([])
#         index = UndefinedLitteral()
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(StopIteration):
#             expr.value(self.eval2)
#
#     def test_evaluated_variable_index_static_list_get_item(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(Variable('X'))
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2), 1)
#
#     def test_evaluated_variable_index_static_linkedlist_get_item(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(Variable('X'))
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2), 1)
#
#     def test_evaluated_variable_index_static_set_get_item(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(Variable('X'))
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2)
#
#     def test_unevaluated_variable_index_static_list_get_item(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(Variable('Y'))
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(ValueError):
#             expr.value(self.eval2)
#
#     def test_unevaluated_variable_index_static_linkedlist_get_item(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(Variable('Y'))
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(ValueError):
#             expr.value(self.eval2)
#
#     def test_unevaluated_variable_index_static_set_get_item(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = ALitteral(Variable('Y'))
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(ValueError):
#             expr.value(self.eval2)
#
#     def test_undefined_index_static_list_get_item(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = UndefinedLitteral()
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2)
#
#     def test_undefined_index_static_linkedlist_get_item(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = UndefinedLitteral()
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2)
#
#     def test_undefined_index_static_set_get_item(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = UndefinedLitteral()
#         expr = GetItemExpression(l, index)
#         self.assertIn(expr.value(self.eval2, 0), [1, 12.0, 'abc'])
#
#     def test_self_litteral_index_static_list_get_item(self):
#         l = ListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = SelfLitteral()
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2, 0), 1)
#
#     def test_self_litteral_index_static_linkedlist_get_item(self):
#         l = LinkedListLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = SelfLitteral()
#         expr = GetItemExpression(l, index)
#         self.assertEqual(expr.value(self.eval2, 0), 1)
#
#     def test_self_litteral_index_static_set_get_item(self):
#         l = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         index = SelfLitteral()
#         expr = GetItemExpression(l, index)
#         with self.assertRaises(TypeError):
#             expr.value(self.eval2, 2)