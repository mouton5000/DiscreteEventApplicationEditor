__author__ = 'mouton'

from unittest import TestCase
from triggerExpressions import *
from arithmeticExpressions import *
from triggerGrammar import TriggerParser
from database import Variable


class TestTriggerGrammarParser(TestCase):

    @classmethod
    def setUpClass(cls):
        import grammar.grammars
        grammar.grammars.compileGrammars()

    def test_parse_litteral_1(self):
        toParse = 'true'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, BLitteral)
        self.assertTrue(expr._value)

    def test_parse_litteral_2(self):
        toParse = 'false'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, BLitteral)
        self.assertFalse(expr._value)

    def test_parse_timer(self):
        toParse = 'timer(30)'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Timer)
        self.assertEqual(expr._nbFrames.value(Evaluation()), 30)

    def test_parse_rand(self):
        toParse = 'rand(0.5)'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Rand)
        self.assertEqual(expr._prob.value(Evaluation()), 0.5)

    def test_parse_randint(self):
        toParse = 'randInt(X, 5)'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, RandInt)
        self.assertIsInstance(expr._var, Variable)
        self.assertEqual(expr._var._name, 'X')
        self.assertEqual(expr._maxInt.value(Evaluation()), 5)

    def test_parse_is(self):
        toParse = 'X is 5'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Is)
        self.assertIsInstance(expr._a1, Variable)
        self.assertEqual(expr._a1._name, 'X')
        self.assertEqual(expr._a2.value(Evaluation()), 5)

    def test_parse_del(self):
        toParse = 'del Y'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Del)
        self.assertIsInstance(expr._a1, Variable)
        self.assertEqual(expr._a1._name, 'Y')

    def test_parse_any(self):
        toParse = 'anyEval(true)'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, AnyEval)
        self.assertIsInstance(expr._expr, BLitteral)
        self.assertEqual(expr._expr._value, True)

    def test_parse_random(self):
        toParse = 'randomEval(true)'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, RandomEval)
        self.assertIsInstance(expr._expr, BLitteral)
        self.assertEqual(expr._expr._value, True)

    def test_parse_min(self):
        toParse = 'minEval[X](true)'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, SelectMinEval)
        self.assertIsInstance(expr._arithmExpr, ALitteral)
        self.assertIsInstance(expr._arithmExpr._value, Variable)
        self.assertEqual(expr._arithmExpr._value._name, 'X')
        self.assertIsInstance(expr._expr, BLitteral)
        self.assertEqual(expr._expr._value, True)

    def test_parse_max(self):
        toParse = 'maxEval[X](true)'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, SelectMaxEval)
        self.assertIsInstance(expr._arithmExpr, ALitteral)
        self.assertIsInstance(expr._arithmExpr._value, Variable)
        self.assertEqual(expr._arithmExpr._value._name, 'X')
        self.assertIsInstance(expr._expr, BLitteral)
        self.assertEqual(expr._expr._value, True)

    def test_parse_and(self):
        toParse = 'true and false'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, And)
        self.assertIsInstance(expr._a1, BLitteral)
        self.assertEqual(expr._a1._value, True)
        self.assertIsInstance(expr._a2, BLitteral)
        self.assertEqual(expr._a2._value, False)

    def test_parse_or(self):
        toParse = 'true or false'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Or)
        self.assertIsInstance(expr._a1, BLitteral)
        self.assertEqual(expr._a1._value, True)
        self.assertIsInstance(expr._a2, BLitteral)
        self.assertEqual(expr._a2._value, False)

    def test_not(self):
        toParse = 'not true'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Not)
        self.assertIsInstance(expr._a1, BLitteral)
        self.assertEqual(expr._a1._value, True)

    def test_parse_parenthesis(self):
        toParse = '((true) or (false))'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Or)
        self.assertIsInstance(expr._a1, BLitteral)
        self.assertEqual(expr._a1._value, True)
        self.assertIsInstance(expr._a2, BLitteral)
        self.assertEqual(expr._a2._value, False)

    def test_parse_compare_leq(self):
        toParse = '0.5 <= 1'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, LeqThan)
        self.assertEqual(expr._a1.value(Evaluation()), 0.5)
        self.assertEqual(expr._a2.value(Evaluation()), 1)

    def test_parse_compare_geq(self):
        toParse = '0.5 >= 1'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, GeqThan)
        self.assertEqual(expr._a1.value(Evaluation()), 0.5)
        self.assertEqual(expr._a2.value(Evaluation()), 1)

    def test_parse_compare_low(self):
        toParse = '0.5 < 1'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, LowerThan)
        self.assertEqual(expr._a1.value(Evaluation()), 0.5)
        self.assertEqual(expr._a2.value(Evaluation()), 1)

    def test_parse_compare_eq(self):
        toParse = '0.5 == 1'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Equals)
        self.assertEqual(expr._a1.value(Evaluation()), 0.5)
        self.assertEqual(expr._a2.value(Evaluation()), 1)

    def test_parse_compare_neq(self):
        toParse = '0.5 != 1'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, NotEquals)
        self.assertEqual(expr._a1.value(Evaluation()), 0.5)
        self.assertEqual(expr._a2.value(Evaluation()), 1)

    def test_parse_empty_property(self):
        toParse = 'pTest()'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, PropertyTriggerExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 0)

    def test_parse_property_args(self):
        toParse = 'pTest(1, 0.5, \'abc\', X)'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, PropertyTriggerExpression)
        self.assertEquals(len(expr._args), 4)
        self.assertEquals(expr._args[0].value(Evaluation()), 1)
        self.assertEquals(expr._args[1].value(Evaluation()), 0.5)
        self.assertEquals(expr._args[2].value(Evaluation()), 'abc')
        self.assertIsInstance(expr._args[3], Variable)
        self.assertEquals(expr._args[3].name, 'X')
        self.assertEquals(len(expr._kwargs), 0)

    def test_parse_property_kwargs(self):
        toParse = 'pTest(1 = 12, \'def\'=0.5, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, PropertyTriggerExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 3)
        d = {key.value(Evaluation()): expr._kwargs[key].value(Evaluation()) for key in expr._kwargs}
        self.assertTrue(1 in d)
        self.assertTrue('def' in d)
        self.assertTrue(3 in d)
        self.assertEquals(d[1], 12)
        self.assertEquals(d['def'], 0.5)
        self.assertEquals(d[3], 'abc')

    def test_parse_property_kwargs_variable(self):
        toParse = 'pTest(1 = X, \'def\'=Y, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, PropertyTriggerExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 3)
        for key in expr._kwargs:
            if key.value(Evaluation()) == 1:
                self.assertIsInstance(expr._kwargs[key], Variable)
                self.assertEquals(expr._kwargs[key].name, 'X')
            if key.value(Evaluation()) == 'def':
                self.assertIsInstance(expr._kwargs[key], Variable)
                self.assertEquals(expr._kwargs[key].name, 'Y')
            if key.value(Evaluation()) == 3:
                self.assertNotIsInstance(expr._kwargs[key], Variable)

    def test_parse_property_args_and_kwargs(self):
        toParse = 'pTest(8, \'ghi\', 1 = 12, \'def\'=0.5, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, PropertyTriggerExpression)
        self.assertEquals(len(expr._args), 2)
        self.assertEquals(expr._args[0].value(Evaluation()), 8)
        self.assertEquals(expr._args[1].value(Evaluation()), 'ghi')
        self.assertEquals(len(expr._kwargs), 3)
        d = {key.value(Evaluation()): expr._kwargs[key].value(Evaluation()) for key in expr._kwargs}
        self.assertTrue(1 in d)
        self.assertTrue('def' in d)
        self.assertTrue(3 in d)
        self.assertEquals(d[1], 12)
        self.assertEquals(d['def'], 0.5)
        self.assertEquals(d[3], 'abc')

    def test_parse_empty_event(self):
        toParse = 'eTest()'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, EventTriggerExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 0)

    def test_parse_event_args(self):
        toParse = 'eTest(1, 0.5, \'abc\', X)'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, EventTriggerExpression)
        self.assertEquals(len(expr._args), 4)
        self.assertEquals(expr._args[0].value(Evaluation()), 1)
        self.assertEquals(expr._args[1].value(Evaluation()), 0.5)
        self.assertEquals(expr._args[2].value(Evaluation()), 'abc')
        self.assertIsInstance(expr._args[3], Variable)
        self.assertEquals(expr._args[3].name, 'X')
        self.assertEquals(len(expr._kwargs), 0)

    def test_parse_event_kwargs(self):
        toParse = 'eTest(1 = 12, \'def\'=0.5, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, EventTriggerExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 3)
        d = {key.value(Evaluation()): expr._kwargs[key].value(Evaluation()) for key in expr._kwargs}
        self.assertTrue(1 in d)
        self.assertTrue('def' in d)
        self.assertTrue(3 in d)
        self.assertEquals(d[1], 12)
        self.assertEquals(d['def'], 0.5)
        self.assertEquals(d[3], 'abc')

    def test_parse_event_kwargs_variable(self):
        toParse = 'eTest(1 = X, \'def\'=Y, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, EventTriggerExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 3)
        for key in expr._kwargs:
            if key.value(Evaluation()) == 1:
                self.assertIsInstance(expr._kwargs[key], Variable)
                self.assertEquals(expr._kwargs[key].name, 'X')
            if key.value(Evaluation()) == 'def':
                self.assertIsInstance(expr._kwargs[key], Variable)
                self.assertEquals(expr._kwargs[key].name, 'Y')
            if key.value(Evaluation()) == 3:
                self.assertNotIsInstance(expr._kwargs[key], Variable)

    def test_parse_event_args_and_kwargs(self):
        toParse = 'eTest(8, \'ghi\', 1 = 12, \'def\'=0.5, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, EventTriggerExpression)
        self.assertEquals(len(expr._args), 2)
        self.assertEquals(expr._args[0].value(Evaluation()), 8)
        self.assertEquals(expr._args[1].value(Evaluation()), 'ghi')
        self.assertEquals(len(expr._kwargs), 3)
        d = {key.value(Evaluation()): expr._kwargs[key].value(Evaluation()) for key in expr._kwargs}
        self.assertTrue(1 in d)
        self.assertTrue('def' in d)
        self.assertTrue(3 in d)
        self.assertEquals(d[1], 12)
        self.assertEquals(d['def'], 0.5)
        self.assertEquals(d[3], 'abc')

    def test_parse_empty_token(self):
        toParse = 'token()'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, TokenExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 0)

    def test_parse_token_args(self):
        toParse = 'token(1, 0.5, \'abc\', X)'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, TokenExpression)
        self.assertEquals(len(expr._args), 4)
        self.assertEquals(expr._args[0].value(Evaluation()), 1)
        self.assertEquals(expr._args[1].value(Evaluation()), 0.5)
        self.assertEquals(expr._args[2].value(Evaluation()), 'abc')
        self.assertIsInstance(expr._args[3], Variable)
        self.assertEquals(expr._args[3].name, 'X')
        self.assertEquals(len(expr._kwargs), 0)

    def test_parse_token_kwargs(self):
        toParse = 'token(1 = 12, \'def\'=0.5, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, TokenExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 3)
        d = {key.value(Evaluation()): expr._kwargs[key].value(Evaluation()) for key in expr._kwargs}
        self.assertTrue(1 in d)
        self.assertTrue('def' in d)
        self.assertTrue(3 in d)
        self.assertEquals(d[1], 12)
        self.assertEquals(d['def'], 0.5)
        self.assertEquals(d[3], 'abc')

    def test_parse_token_kwargs_variable(self):
        toParse = 'token(1 = X, \'def\'=Y, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, TokenExpression)
        self.assertEquals(len(expr._args), 0)
        self.assertEquals(len(expr._kwargs), 3)
        for key in expr._kwargs:
            if key.value(Evaluation()) == 1:
                self.assertIsInstance(expr._kwargs[key], Variable)
                self.assertEquals(expr._kwargs[key].name, 'X')
            if key.value(Evaluation()) == 'def':
                self.assertIsInstance(expr._kwargs[key], Variable)
                self.assertEquals(expr._kwargs[key].name, 'Y')
            if key.value(Evaluation()) == 3:
                self.assertNotIsInstance(expr._kwargs[key], Variable)

    def test_parse_token_args_and_kwargs(self):
        toParse = 'token(8, \'ghi\', 1 = 12, \'def\'=0.5, 3=\'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, TokenExpression)
        self.assertEquals(len(expr._args), 2)
        self.assertEquals(expr._args[0].value(Evaluation()), 8)
        self.assertEquals(expr._args[1].value(Evaluation()), 'ghi')
        self.assertEquals(len(expr._kwargs), 3)
        d = {key.value(Evaluation()): expr._kwargs[key].value(Evaluation()) for key in expr._kwargs}
        self.assertTrue(1 in d)
        self.assertTrue('def' in d)
        self.assertTrue(3 in d)
        self.assertEquals(d[1], 12)
        self.assertEquals(d['def'], 0.5)
        self.assertEquals(d[3], 'abc')

    def test_parse_eLock_empty(self):
        toParse = 'eLock(1)'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, eLock)
        self.assertEqual(expr._priority.value(Evaluation()), 1)
        self.assertEquals(len(expr._keys), 0)

    def test_parse_eLock_args(self):
        toParse = 'eLock(-1, 1, 0.5, \'abc\')'
        expr = TriggerParser.parse(toParse)
        self.assertIsInstance(expr, eLock)
        self.assertEqual(expr._priority.value(Evaluation()), -1)
        self.assertEquals(len(expr._keys), 3)
        self.assertEquals(expr._keys[0].value(Evaluation()), 1)
        self.assertEquals(expr._keys[1].value(Evaluation()), 0.5)
        self.assertEquals(expr._keys[2].value(Evaluation()), 'abc')

    def test_parse_complicate_and_or(self):
        toParse = 'true and false or true and false'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, Or)
        self.assertIsInstance(expr._a1, And)
        self.assertIsInstance(expr._a1._a1, BLitteral)
        self.assertEqual(expr._a1._a1._value, True)
        self.assertIsInstance(expr._a1._a2, BLitteral)
        self.assertEqual(expr._a1._a2._value, False)
        self.assertIsInstance(expr._a2, And)
        self.assertIsInstance(expr._a2._a1, BLitteral)
        self.assertEqual(expr._a2._a1._value, True)
        self.assertIsInstance(expr._a2._a2, BLitteral)
        self.assertEqual(expr._a2._a2._value, False)

    def test_parse_complicate_and_or_2(self):
        toParse = 'true and (false or true) and false'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, And)
        self.assertIsInstance(expr._a1, BLitteral)
        self.assertEqual(expr._a1._value, True)
        self.assertIsInstance(expr._a2, And)
        self.assertIsInstance(expr._a2._a1, Or)
        self.assertIsInstance(expr._a2._a1._a1, BLitteral)
        self.assertEqual(expr._a2._a1._a1._value, False)
        self.assertIsInstance(expr._a2._a1._a2, BLitteral)
        self.assertEqual(expr._a2._a1._a2._value, True)
        self.assertIsInstance(expr._a2._a2, BLitteral)
        self.assertEqual(expr._a2._a2._value, False)

    def test_parse_complicate_expression(self):
        toParse = 'anyEval(X is 2 and not timer(30) or (Y is 3 and pTest(X,2=Y) or eTest(X, 2)))'
        expr = TriggerParser.parse(toParse)

        self.assertIsInstance(expr, AnyEval)
        self.assertIsInstance(expr._expr, Or)
        self.assertIsInstance(expr._expr._a1, And)
        self.assertIsInstance(expr._expr._a1._a1, Is)
        self.assertIsInstance(expr._expr._a1._a2, Not)
        self.assertIsInstance(expr._expr._a1._a2._a1, Timer)
        self.assertIsInstance(expr._expr._a2, Or)
        self.assertIsInstance(expr._expr._a2._a1, And)
        self.assertIsInstance(expr._expr._a2._a1._a1, Is)
        self.assertIsInstance(expr._expr._a2._a1._a2, PropertyTriggerExpression)
        self.assertIsInstance(expr._expr._a2._a2, EventTriggerExpression)