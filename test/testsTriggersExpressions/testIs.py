__author__ = 'mouton'

from unittest import TestCase

from triggerExpressions import Evaluation, Is
from database import Variable
from test.testsTriggersExpressions import simpleTests
from arithmeticExpressions import ALitteral


class TestIs(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

    def setUp(self):
        self.eval1 = Evaluation()
        self.eval2 = Evaluation()
        self.eval2[Variable('X')] = 1
        self.eval2[Variable('Y')] = 'abc'
        self.eval2[Variable('Z')] = 12.0
        self.eval2[Variable('T')] = True

    def test_integer_is_with_empty_previous_evaluation(self):
        self.is_with_empty_previous_evaluation(1)

    def test_float_is_with_empty_previous_evaluation(self):
        self.is_with_empty_previous_evaluation(1.0)

    def test_string_is_with_empty_previous_evaluation(self):
        self.is_with_empty_previous_evaluation('abc')

    def test_boolean_is_with_empty_previous_evaluation(self):
        self.is_with_empty_previous_evaluation(True)

    def is_with_empty_previous_evaluation(self, isValue):
        trig = Is(Variable('X'), ALitteral(isValue))

        evaluation = Evaluation()
        evaluation[Variable('X')] = isValue

        simpleTests.test_evaluation(self, trig, self.eval1, None, evaluation)

    def test_integer_is_false_with_empty_previous_evaluation(self):
        self.is_false_with_non_empty_previous_evaluation(42)

    def test_float_is_false_with_empty_previous_evaluation(self):
        self.is_false_with_non_empty_previous_evaluation(3.14)

    def test_string_is_false_with_empty_previous_evaluation(self):
        self.is_false_with_non_empty_previous_evaluation('zywx')

    def test_boolean_is_false_with_empty_previous_evaluation(self):
        self.is_false_with_non_empty_previous_evaluation(True)

    def is_false_with_non_empty_previous_evaluation(self, isValue):
        trig = Is(Variable('X'), ALitteral(isValue))

        simpleTests.test_evaluation(self, trig, self.eval2, None)

    def test_integer_is_true_with_empty_previous_evaluation(self):
        self.is_true_with_non_empty_previous_evaluation(-42)

    def test_float_is_true_with_empty_previous_evaluation(self):
        self.is_true_with_non_empty_previous_evaluation(6.0231023)

    def test_string_is_true_with_empty_previous_evaluation(self):
        self.is_true_with_non_empty_previous_evaluation('abcdefgh')

    def test_boolean_is_true_with_empty_previous_evaluation(self):
        self.is_true_with_non_empty_previous_evaluation(False)

    def is_true_with_non_empty_previous_evaluation(self, isValue):
        trig = Is(Variable('J'), ALitteral(isValue))

        evaluation = Evaluation()
        evaluation[Variable('X')] = 1
        evaluation[Variable('Y')] = 'abc'
        evaluation[Variable('Z')] = 12.0
        evaluation[Variable('T')] = True
        evaluation[Variable('J')] = isValue

        simpleTests.test_evaluation(self, trig, self.eval2, None, evaluation)