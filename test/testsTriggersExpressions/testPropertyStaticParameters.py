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
        
    def test_success_empty_property_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empty', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_success_empty_property_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empty', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_wrong_name_1_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empti', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_wrong_name_1_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('Empti', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)
    #
    # def test_fail_wrong_args_1_with_empty_previous_evaluation(self):
    #     trig = PropertyTriggerExpression('Empty', [1], {})
    #     token = None
    #     simpleTests.test_evaluation(self, trig, self.eval1, token)
    #
    # def test_fail_wrong_args_1_with_non_empty_previous_evaluation(self):
    #     trig = PropertyTriggerExpression('Empty', [1], {})
    #     token = None
    #     simpleTests.test_evaluation(self, trig, self.eval2, token)
    #
    # def test_fail_wrong_kwargs_1_with_empty_previous_evaluation(self):
    #     trig = PropertyTriggerExpression('Empty', [], {1: 2})
    #     token = None
    #     simpleTests.test_evaluation(self, trig, self.eval1, token)
    #
    # def test_fail_wrong_kwargs_1_with_non_empty_previous_evaluation(self):
    #     trig = PropertyTriggerExpression('Empty', [], {'abc': 3})
    #     token = None
    #     simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_integer_property_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_success_integer_property_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [ALitteral(2)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_wrong_name_2_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('J', [ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_wrong_name_2_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('J', [ALitteral(2)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_wrong_args_2_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [ALitteral(3)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_wrong_args_2_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [ALitteral(-2)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    # def test_fail_wrong_kwargs_2_with_empty_previous_evaluation(self):
    #     trig = PropertyTriggerExpression('I', [ALitteral(1)], {ALitteral(2): ALitteral(1)})
    #     token = None
    #     simpleTests.test_evaluation(self, trig, self.eval1, token)
    #
    # def test_fail_wrong_kwargs_2_with_non_empty_previous_evaluation(self):
    #     trig = PropertyTriggerExpression('I', [ALitteral(2)], {ALitteral(1): ALitteral('abc')})
    #     token = None
    #     simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_float_property_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(1), ALitteral(pi)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_success_float_property_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(2), ALitteral(pi)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_float_property_2_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(1), ALitteral(sqrt(2))], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_string_property_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('SSI', [ALitteral('machin'), ALitteral('truc'), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_success_string_property_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('SSI', [ALitteral('machin'), ALitteral('bidule'), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_multiple_types_property_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('MultipleTypes', [ALitteral('machin')], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_multiple_types_property_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('MultipleTypes', [ALitteral(12)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_success_multiple_types_2_property_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('MultipleTypes', [ALitteral(1.0)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_integer_float_equality_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('MultipleTypes', [ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_float_integer_equality_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('MultipleTypes', [ALitteral(12.0)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token, self.eval1)

    def test_fail_too_many_args_1_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [ALitteral(1), ALitteral(2)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_too_many_args_1_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [ALitteral(2), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_not_enough_args_1_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_not_enough_args_1_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('I', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_swapped_args_1_with_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(pi), ALitteral(1)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval1, token)

    def test_fail_swapped_args_1_with_non_empty_previous_evaluation(self):
        trig = PropertyTriggerExpression('IF', [ALitteral(pi), ALitteral(2)], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_kwargs_integer_integer(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_not_enough_kwargs(self):
        trig = PropertyTriggerExpression('EII', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_integer_integer_integer_float_equality(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1.0): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_integer_integer_integer_float_equality_2(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1): ALitteral(12.0)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_fail_wrong_kwargs(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(2): ALitteral('abc')})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_swap_key_and_value(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(12): ALitteral(1)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_fail_too_many_kwargs(self):
        trig = PropertyTriggerExpression('EII', [], {ALitteral(1): ALitteral(12), ALitteral(2): ALitteral(24)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token)

    def test_success_kwargs_integer_float(self):
        trig = PropertyTriggerExpression('EIF', [], {ALitteral(1): ALitteral(pi)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_integer_string(self):
        trig = PropertyTriggerExpression('EIS', [], {ALitteral(1): ALitteral('def')})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_float_integer(self):
        trig = PropertyTriggerExpression('EFI', [], {ALitteral(sqrt(2)): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_float_float(self):
        trig = PropertyTriggerExpression('EFF', [], {ALitteral(sqrt(2)): ALitteral(pi)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_float_string(self):
        trig = PropertyTriggerExpression('EFS', [], {ALitteral(sqrt(2)): ALitteral('def')})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_string_integer(self):
        trig = PropertyTriggerExpression('ESI', [], {ALitteral('abc'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_string_float(self):
        trig = PropertyTriggerExpression('ESF', [], {ALitteral('abc'): ALitteral(pi)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_kwargs_string_string(self):
        trig = PropertyTriggerExpression('ESS', [], {ALitteral('abc'): ALitteral('def')})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(1): ALitteral(12), ALitteral('abc'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_swap_two_kwargs(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral('abc'): ALitteral(12), ALitteral(1): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_2(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(1): ALitteral(12), ALitteral('abc'): ALitteral(13)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_3(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(1): ALitteral(12), ALitteral('def'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_not_enough_kwargs(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral(1): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_two_kwargs_not_enough_kwargs_2(self):
        trig = PropertyTriggerExpression('ETwoKW', [], {ALitteral('def'): ALitteral(12)})
        token = None
        print Property.properties
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs(self):
        trig = PropertyTriggerExpression('Any', [], {})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_2(self):
        trig = PropertyTriggerExpression('Any', [ALitteral(3), ALitteral(2)],
                                         {ALitteral(1): ALitteral(12), ALitteral('abc'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_3(self):
        trig = PropertyTriggerExpression('Any', [ALitteral(1), ALitteral(1)],
                                         {ALitteral(1): ALitteral(12), ALitteral('abc'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_4(self):
        trig = PropertyTriggerExpression('Any', [ALitteral(2), ALitteral(1)],
                                         {ALitteral(1): ALitteral(12), ALitteral('abc'): ALitteral(12)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_5(self):
        trig = PropertyTriggerExpression('Any', [ALitteral('def'), ALitteral(pi), ALitteral(3)],
                                         {ALitteral(4): ALitteral(1.0), ALitteral('abc'): ALitteral(pi)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)

    def test_success_any_args_kwargs_6(self):
        trig = PropertyTriggerExpression('Any', [ALitteral(pi), ALitteral(3), ALitteral(3)],
                                         {ALitteral(4): ALitteral(1.0), ALitteral('abc'): ALitteral(pi)})
        token = None
        simpleTests.test_evaluation(self, trig, self.eval2, token, self.eval2)