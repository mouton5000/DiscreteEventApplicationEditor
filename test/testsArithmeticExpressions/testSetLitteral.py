# __author__ = 'mouton'
#
# from arithmeticExpressions import ALitteral, SetLitteral, UndefinedLitteral, SelfLitteral
# from triggerExpressions import Evaluation
# from database import Variable, UNDEFINED_PARAMETER
# from unittest import TestCase
#
#
# class TestSetLitteral(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         import grammar.grammars
#         grammar.grammars.compileGrammars()
#
#     def setUp(self):
#         self.eval1 = Evaluation()
#         self.eval2 = Evaluation()
#         self.eval2[Variable('X')] = 1
#         self.eval2[Variable('T')] = 'abc'
#         self.eval2[Variable('Z')] = 12.0
#
#     def test_empty_list_with_empty_evaluation(self):
#         expr = SetLitteral([])
#         self.assertEqual(expr.value(self.eval1), set([]))
#
#     def test_empty_list_with_non_empty_evaluation(self):
#         expr = SetLitteral([])
#         self.assertEqual(expr.value(self.eval2), set([]))
#
#     def test_static_list_with_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         self.assertEqual(expr.value(self.eval1), set([1, 12.0, 'abc', 12.0]))
#
#     def test_static_list_with_non_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(12.0), ALitteral('abc'), ALitteral(12.0)])
#         self.assertEqual(expr.value(self.eval2), set([1, 12.0, 'abc', 12.0]))
#
#     def test_undefined_list_with_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(12.0), UndefinedLitteral(),
#                                     ALitteral('abc'), UndefinedLitteral()])
#         self.assertEqual(expr.value(self.eval1), set([1, 12.0, 'abc', UNDEFINED_PARAMETER]))
#
#     def test_undefined_list_with_non_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(12.0), UndefinedLitteral(),
#                                     ALitteral('abc'), UndefinedLitteral()])
#         self.assertEqual(expr.value(self.eval2), set([1, 12.0, 'abc', UNDEFINED_PARAMETER]))
#
#     def test_evaluated_variable_list_with_non_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(Variable('X')), ALitteral(Variable('X')), ALitteral(12.0)])
#         self.assertEqual(expr.value(self.eval2), set([1, 12.0]))
#
#     def test_unevaluated_variable_list_with_non_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(Variable('Y')), ALitteral(Variable('X')), ALitteral(12.0)])
#         with self.assertRaises(ValueError):
#             expr.value(self.eval2)
#
#     def test_self_litteral_list_with_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(12.0), SelfLitteral(),
#                                     ALitteral('abc'), SelfLitteral()])
#         self.assertEqual(expr.value(self.eval1, 'def'), set([1, 12.0, 'def', 'abc']))
#
#     def test_self_litteral_list_with_non_empty_evaluation(self):
#         expr = SetLitteral([ALitteral(1), ALitteral(12.0), SelfLitteral(),
#                                     ALitteral('abc'), SelfLitteral()])
#         self.assertEqual(expr.value(self.eval2, 'def'), set([1, 12.0, 'def', 'abc']))