__author__ = 'mouton'

from unittest import TestCase

from triggerExpressions import Rand, Evaluation
from database import Variable
from test.testsTriggersExpressions import simpleTests
from arithmeticExpressions import ALitteral


class TestRand(TestCase):
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

    def test_rand_one_with_empty_previous_evaluation(self):
        rand = Rand(ALitteral(1.0))
        for i in xrange(100):
            simpleTests.test_evaluation(self, rand, self.eval1, None, self.eval1)

    def test_rand_one_with_non_empty_previous_evaluation(self):
        rand = Rand(ALitteral(1.0))
        for i in xrange(100):
            simpleTests.test_evaluation(self, rand, self.eval2, None, self.eval2)

    def test_rand_true_with_empty_previous_evaluation(self):
        self.rand_true(self.eval1)

    def test_rand_true_with_none_empty_previous_evaluation(self):
        self.rand_true(self.eval2)

    def rand_true(self, previousEvaluation):
        rand = Rand(ALitteral(0.5))
        import random
        random.seed(0)

        random.random()
        random.random()
        simpleTests.test_evaluation(self, rand, previousEvaluation, None, previousEvaluation)
        simpleTests.test_evaluation(self, rand, previousEvaluation, None, previousEvaluation)
        random.random()
        simpleTests.test_evaluation(self, rand, previousEvaluation, None, previousEvaluation)
        random.random()
        simpleTests.test_evaluation(self, rand, previousEvaluation, None, previousEvaluation)
        simpleTests.test_evaluation(self, rand, previousEvaluation, None, previousEvaluation)
        random.random()

    def test_rand_zero_with_empty_previous_evaluation(self):
        rand = Rand(ALitteral(0))
        for i in xrange(100):
            simpleTests.test_evaluation(self, rand, self.eval1, None)

    def test_rand_zero_with_non_empty_previous_evaluation(self):
        rand = Rand(ALitteral(0))
        for i in xrange(100):
            simpleTests.test_evaluation(self, rand, self.eval2, None)

    def test_rand_false_with_empty_previous_evaluation(self):
        self.rand_false(self.eval1)

    def test_rand_false_with_non_empty_previous_evaluation(self):
        self.rand_false(self.eval2)

    def rand_false(self, previousEvaluation):
        rand = Rand(ALitteral(0.5))
        import random
        random.seed(0)

        simpleTests.test_evaluation(self, rand, previousEvaluation, None)
        simpleTests.test_evaluation(self, rand, previousEvaluation, None)
        random.random()
        random.random()
        simpleTests.test_evaluation(self, rand, previousEvaluation, None)
        random.random()
        simpleTests.test_evaluation(self, rand, previousEvaluation, None)
        random.random()
        random.random()
        simpleTests.test_evaluation(self, rand, previousEvaluation, None)