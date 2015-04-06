__author__ = 'mouton'

from arithmeticExpressions import ALitteral, UndefinedLitteral
from unittest import TestCase
from triggerExpressions import Evaluation, PropertyTriggerExpression
from database import Variable, Property
from test.testsTriggersExpressions import simpleTests
from math import pi, sqrt


class TestUndefinedPropertyTriggerExpression(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

        Property.properties.clear()

        Property.add('Empty', [], {})
        Property.add('I', [1], {})
        Property.add('I', [2], {})
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
        self.eval1 = Evaluation()
        self.eval2 = Evaluation()
        self.eval2[Variable('X')] = 1
        self.eval2[Variable('Y')] = 'abc'
        self.eval2[Variable('Z')] = 12.0
        self.eval2[Variable('T')] = True

    def test_fail_too_many_args_1_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empty', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_too_many_args_1_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empty', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_too_many_kwargs_1_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empty', [], {1: UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_too_many_kwargs_1_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empty', [], {2: UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_integer_property_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_fail_wrong_name_2_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('J', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_wrong_name_2_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('J', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_two_args(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(1), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_success_two_args_2(self):
        trig = PropertyTriggerExpression('IF', [UndefinedLitteral(), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_success_two_args_3(self):
        trig = PropertyTriggerExpression('IF', [UndefinedLitteral(), ALitteral(pi)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_fail_wrong_args_1(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(3), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_wrong_args_2(self):
        trig = PropertyTriggerExpression('IF', [UndefinedLitteral(), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_success_three_args(self):
        trig = PropertyTriggerExpression('SSI', [ALitteral('machin'), ALitteral('truc'), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_three_args_2(self):
        trig = PropertyTriggerExpression('SSI', [ALitteral('machin'), UndefinedLitteral(), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_three_args_3(self):
        trig = PropertyTriggerExpression('SSI', [UndefinedLitteral(), ALitteral('truc'), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_three_args_4(self):
        trig = PropertyTriggerExpression('SSI', [ALitteral('machin'), UndefinedLitteral(), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_three_args_5(self):
        trig = PropertyTriggerExpression('SSI', [UndefinedLitteral(), UndefinedLitteral(), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_three_args_6(self):
        trig = PropertyTriggerExpression('SSI', [UndefinedLitteral(), UndefinedLitteral(), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_not_enough_args_1(self):
        trig = PropertyTriggerExpression('SSI', [UndefinedLitteral(), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_not_enough_args_2(self):
        trig = PropertyTriggerExpression('SSI', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_too_many_args_2(self):
        trig = PropertyTriggerExpression('SSI', [ALitteral('machin'), ALitteral('truc'),
                                                 ALitteral(1), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_too_many_args_3(self):
        trig = PropertyTriggerExpression('SSI', [UndefinedLitteral(), UndefinedLitteral(),
                                                 UndefinedLitteral(), UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_swap_args(self):
        trig = PropertyTriggerExpression('SSI', [UndefinedLitteral(), ALitteral('machin'), ALitteral('truc')], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_multiple_types_property_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('MultipleTypes', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_integer_integer(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_integer_integer_integer_float_equality(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1.0): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_wrong_kwargs(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(2): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_swap_key_and_value(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(12): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_too_many_kwargs(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1): UndefinedLitteral(), ALitteral(2): ALitteral(24)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_too_many_kwargs_2(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1): ALitteral(12), ALitteral(2): UndefinedLitteral})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_undefined_key(self):
        trig = PropertyTriggerExpression('EII', [], {UndefinedLitteral(): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_two_kwargs(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(1): UndefinedLitteral(),
                                                        ALitteral('abc'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_swap_two_kwargs(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral('abc'): UndefinedLitteral(),
                                                        ALitteral(1): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_2(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(1): UndefinedLitteral(),
                                                        ALitteral('abc'): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_not_enough_kwargs(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(1): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_not_enough_kwargs_2(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral('abc'): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_not_enough_kwargs_3(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral('def'): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_any_args_kwargs(self):
        trig = PropertyTriggerExpression('Any', [UndefinedLitteral()], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_any_args_kwargs_2(self):
        trig = PropertyTriggerExpression('Any', [UndefinedLitteral(), UndefinedLitteral()],
                                         {ALitteral(1): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_3(self):
        trig = PropertyTriggerExpression('Any', [UndefinedLitteral(), UndefinedLitteral()],
                                         {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_4(self):
        trig = PropertyTriggerExpression('Any', [UndefinedLitteral(), UndefinedLitteral()],
                                         {ALitteral(1): ALitteral(12), ALitteral('abc'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_5(self):
        trig = PropertyTriggerExpression('Any', [UndefinedLitteral(), ALitteral(pi), UndefinedLitteral()],
                                         {ALitteral(4): UndefinedLitteral(), ALitteral('abc'): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_6(self):
        trig = PropertyTriggerExpression('Any', [UndefinedLitteral(), UndefinedLitteral(), UndefinedLitteral()],
                                         {ALitteral(4): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_any_args_kwargs_6(self):
        trig = PropertyTriggerExpression('Any', [UndefinedLitteral(), UndefinedLitteral(), UndefinedLitteral()],
                                         {ALitteral(5): UndefinedLitteral()})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)