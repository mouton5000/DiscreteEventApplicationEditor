__author__ = 'mouton'

from unittest import TestCase

from triggerExpressions import RandInt, Evaluation
from database import Variable
from test.testsTriggersExpressions import simpleTests
from arithmeticExpressions import ALitteral


class TestRandInt(TestCase):
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

    def test_succeed_randInt_with_constant_expected_result_with_empty_previous_evaluation(self):
        self.succeed_randInt_with_constant_expected_result(self.eval1)

    def test_succeed_randInt_with_constant_expected_result_with_non_empty_previous_evaluation(self):
        self.succeed_randInt_with_constant_expected_result(self.eval2)

    def succeed_randInt_with_constant_expected_result(self, previousEvaluation):
        import random

        random.seed(0)
        maxInt = ALitteral(3)

        expected_result = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        expected_result = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        expected_result = ALitteral(1)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        expected_result = ALitteral(0)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        expected_result = ALitteral(1)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

    def test_failed_randInt_with_constant_expected_result_with_empty_previous_evaluation(self):
        self.failed_randInt_with_constant_expected_result(self.eval1)

    def test_failed_randInt_with_constant_expected_result_with_non_empty_previous_evaluation(self):
        self.failed_randInt_with_constant_expected_result(self.eval2)

    def failed_randInt_with_constant_expected_result(self, previousEvaluation):
        import random

        random.seed(0)
        maxInt = ALitteral(3)

        expected_result = ALitteral(1)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(0)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(0)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

    def test_succeed_randInt_with_variable_expected_result(self):
        import random

        random.seed(0)
        maxInt = ALitteral(3)

        previousEvaluation = self.eval2
        expected_result = Variable('X')

        self.eval2[Variable('X')] = 2
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        self.eval2[Variable('X')] = 2
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        self.eval2[Variable('X')] = 1
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        self.eval2[Variable('X')] = 0
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

        self.eval2[Variable('X')] = 1
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, previousEvaluation)

    def test_failed_randInt_with_variable_expected_result(self):
        import random

        random.seed(0)
        maxInt = ALitteral(3)

        previousEvaluation = self.eval2
        expected_result = Variable('X')

        self.eval2[Variable('X')] = 1
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        self.eval2[Variable('X')] = 0
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        self.eval2[Variable('X')] = 2
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        self.eval2[Variable('X')] = 2
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        self.eval2[Variable('X')] = 0
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

    def test_succeed_randInt_with_unevaluated_variable_result_with_empty_previous_evaluation(self):
        self.succeed_randInt_with_unevaluated_variable_result(self.eval1)

    def test_succeed_randInt_with_unevaluated_variable_with_non_empty_previous_evaluation(self):
        self.succeed_randInt_with_unevaluated_variable_result(self.eval2)

    def succeed_randInt_with_unevaluated_variable_result(self, previousEvaluation):
        import random

        random.seed(0)
        maxInt = ALitteral(3)

        evaluation = previousEvaluation.copy()
        evaluation[Variable('J')] = 2
        trig = RandInt(Variable('J'), maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, evaluation)

        evaluation[Variable('J')] = 2
        trig = RandInt(Variable('J'), maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, evaluation)

        evaluation[Variable('J')] = 1
        trig = RandInt(Variable('J'), maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, evaluation)

        evaluation[Variable('J')] = 0
        trig = RandInt(Variable('J'), maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, evaluation)

        evaluation[Variable('J')] = 1
        trig = RandInt(Variable('J'), maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None, evaluation)

    def test_randInd_maxInt_with_constant_expected_result_must_be_positive_with_empty_previous_evaluation(self):
        self.randInd_maxInt_with_constant_expected_result_must_be_positive(self.eval1)

    def test_randInd_maxInt_with_constant_expected_result_must_be_positive_with_non_empty_previous_evaluation(self):
        self.randInd_maxInt_with_constant_expected_result_must_be_positive(self.eval2)

    def randInd_maxInt_with_constant_expected_result_must_be_positive(self, previousEvaluation):
        maxInt = ALitteral(-2)
        import random

        random.seed(0)
        expected_result = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(1)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(0)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

        expected_result = ALitteral(1)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)

    def test_randInd_maxInt_with_variable_expected_result_must_be_positive(self):
        maxInt = ALitteral(-2)
        import random
        random.seed(0)

        expected_result = Variable('X')

        self.eval2[Variable('X')] = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, self.eval2, None)

        self.eval2[Variable('X')] = ALitteral(2)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, self.eval2, None)

        self.eval2[Variable('X')] = ALitteral(1)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, self.eval2, None)

        self.eval2[Variable('X')] = ALitteral(0)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, self.eval2, None)

        self.eval2[Variable('X')] = ALitteral(1)
        trig = RandInt(expected_result, maxInt)
        simpleTests.test_evaluation(self, trig, self.eval2, None)

    def test_randInd_maxInt_with_unevaluated_variable_must_be_positive_with_empty_previous_evaluation(self):
        self.randInd_maxInt_with_unevaluated_variable_must_be_positive(self.eval1)

    def test_randInd_maxInt_with_unevaluated_variable_must_be_positive_with_non_empty_previous_evaluation(self):
        self.randInd_maxInt_with_unevaluated_variable_must_be_positive(self.eval2)

    def randInd_maxInt_with_unevaluated_variable_must_be_positive(self, previousEvaluation):
        maxInt = ALitteral(-2)

        trig = RandInt(Variable('J'), maxInt)
        simpleTests.test_evaluation(self, trig, previousEvaluation, None)