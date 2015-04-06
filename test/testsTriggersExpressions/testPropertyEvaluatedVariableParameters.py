from arithmeticExpressions import ALitteral

__author__ = 'mouton'

from unittest import TestCase
from triggerExpressions import BLitteral, Evaluation, PropertyTriggerExpression
from database import Variable, Property
from test.testsTriggersExpressions import simpleTests
from math import pi, sqrt


class TestPropertyTriggerExpression(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

        Property.properties.clear()

        Property.add('Empty', [], {})
        Property.add('I', [1], {})
        Property.add('I', [2], {})
        Property.add('I', [12], {})
        Property.add('IF', [1, pi], {})
        Property.add('IF', [2, pi], {})
        Property.add('IF', [1, sqrt(2)], {})
        Property.add('SSI', ['machin', 'truc', 1], {})
        Property.add('SSI', ['machin', 'bidule', 1], {})
        Property.add('MultipleTypes', ['machin'], {})
        Property.add('MultipleTypes', [12], {})
        Property.add('MultipleTypes', [1.0], {})

        Property.add('EII', [], {1: 12})
        Property.add('EIF', [], {1: pi})
        Property.add('EIS', [], {1: 'def'})
        Property.add('EFI', [], {sqrt(2): 12})
        Property.add('EFF', [], {sqrt(2): pi})
        Property.add('EFS', [], {sqrt(2): 'def'})
        Property.add('ESI', [], {'abc': 12})
        Property.add('ESF', [], {'abc': pi})
        Property.add('ESS', [], {'abc': 'def'})

        Property.add('ETwoKW', [], {1: 12, 'abc': 12})
        Property.add('ETwoKW', [], {1: 12, 'abc': 13})
        Property.add('ETwoKW', [], {1: 12, 'def': 12})
        Property.add('Any', [], {})
        Property.add('Any', [3, 2], {1: 12, 'abc': 12})
        Property.add('Any', [1, 1], {'abc': 12, 1: 12})
        Property.add('Any', [2, 1], {1: 12, 'abc': 12})
        Property.add('Any', ['def', pi, 3], {4: 1.0, 'abc': pi})
        Property.add('Any', [pi, 3, 3], {4: 1.0, 'abc': pi})
        
    def setUp(self):
        self.eval2 = Evaluation()
        self.eval2[Variable('X1')] = 1
        self.eval2[Variable('X2')] = 2
        self.eval2[Variable('X3')] = 3
        self.eval2[Variable('Y')] = 'abc'
        self.eval2[Variable('Z1')] = 12.0
        self.eval2[Variable('Z2')] = pi
        self.eval2[Variable('T')] = 42
        
    def test_success_integer_property(self):
        trig = PropertyTriggerExpression('I', [ALitteral(Variable('X1'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_integer_property_1(self):
        trig = PropertyTriggerExpression('I', [ALitteral(Variable('X2'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_integer_property(self):
        trig = PropertyTriggerExpression('I', [ALitteral(Variable('X3'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_integer_property_1(self):
        trig = PropertyTriggerExpression('I', [ALitteral(Variable('Y'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_integer_property_3(self):
        trig = PropertyTriggerExpression('I', [ALitteral(Variable('Z1'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_integer_property_3(self):
        trig = PropertyTriggerExpression('I', [ALitteral(Variable('Z2'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_integer_property_4(self):
        trig = PropertyTriggerExpression('I', [ALitteral(Variable('T'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_wrong_name(self):
        trig = PropertyTriggerExpression('J', [ALitteral(Variable('X1'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_multiple_parameters_property_1(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(Variable('X1')), ALitteral(Variable('Z2'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_multiple_parameters_property_2(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(Variable('X2')), ALitteral(Variable('Z2'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_multiple_parameters_property_1(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(Variable('X3')), ALitteral(Variable('Z2'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_multiple_parameters_property_2(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(Variable('Z2')), ALitteral(Variable('X1'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_multiple_parameters_property_3(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(Variable('X1'))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_kwargs_1(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(Variable('X1')): ALitteral(Variable('Z1'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_2(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(Variable('Y')): ALitteral(Variable('Z1'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_3(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(Variable('X1')): ALitteral(Variable('Z1')),
                                                        ALitteral(Variable('Y')): ALitteral(Variable('Z1'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_4(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(Variable('Y')): ALitteral(Variable('Z1')),
                                                        ALitteral(Variable('X1')): ALitteral(Variable('Z1'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_kwargs_1(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(Variable('X2')): ALitteral(Variable('Z1')),
                                                        ALitteral(Variable('X1')): ALitteral(Variable('Z1'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_kwargs_2(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(Variable('Y')): ALitteral(Variable('Z2'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_kwargs_3(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(Variable('X1')): ALitteral(Variable('Z1')),
                                                        ALitteral(Variable('Y')): ALitteral(Variable('Z1')),
                                                        ALitteral(Variable('T')): ALitteral(Variable('Z2'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_kwargs_4(self):
        trig = PropertyTriggerExpression('ETwoKW', [ALitteral(Variable('X1'))],
                                                        {ALitteral(Variable('X1')): ALitteral(Variable('Z1')),
                                                         ALitteral(Variable('Y')): ALitteral(Variable('Z1'))})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)