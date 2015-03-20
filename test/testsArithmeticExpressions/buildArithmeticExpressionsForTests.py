__author__ = 'mouton'

from arithmeticExpressions import ALitteral, UndefinedLitteral, Addition, Subtraction
from math import pi, sqrt
from database import Variable


def getAdditionOf10And20():
    a1 = ALitteral(10)
    a2 = ALitteral(20)
    return Addition(a1, a2)


def getAdditionOfABCAndDEF():
    a1 = ALitteral('abc')
    a2 = ALitteral('def')
    return Addition(a1, a2)


def getAdditionOfPiAndSQRT2():
    a1 = ALitteral(pi)
    a2 = ALitteral(sqrt(2))
    return Addition(a1, a2)


def getAdditionOfABCAnd20():
    a1 = ALitteral('abc')
    a2 = ALitteral(20)
    return Addition(a1, a2)


def getAdditionOf10AndDEF():
    a1 = ALitteral(10)
    a2 = ALitteral('def')
    return Addition(a1, a2)


def getAdditionOfPiAnd20():
    a1 = ALitteral(pi)
    a2 = ALitteral(20)
    return Addition(a1, a2)


def getAdditionOf10AndSQRT2():
    a1 = ALitteral(10)
    a2 = ALitteral(sqrt(2))
    return Addition(a1, a2)


def getAdditionOfPiAndDEF():
    a1 = ALitteral(pi)
    a2 = ALitteral('def')
    return Addition(a1, a2)


def getAdditionOfABCAndSQRT2():
    a1 = ALitteral('abc')
    a2 = ALitteral(sqrt(2))
    return Addition(a1, a2)


def getAdditionOf10AndUndefined():
    a1 = ALitteral(10)
    a2 = UndefinedLitteral()
    return Addition(a1, a2)


def getAdditionOfUndefinedAnd20():
    a1 = UndefinedLitteral()
    a2 = ALitteral(20)
    return Addition(a1, a2)


def getAdditionOfABCAndUndefined():
    a1 = ALitteral('abc')
    a2 = UndefinedLitteral()
    return Addition(a1, a2)


def getAdditionOfUndefinedAndDEF():
    a1 = UndefinedLitteral()
    a2 = ALitteral('def')
    return Addition(a1, a2)


def getAdditionOfPiAndUndefined():
    a1 = ALitteral(pi)
    a2 = UndefinedLitteral()
    return Addition(a1, a2)


def getAdditionOfUndefinedAndSQRT2():
    a1 = UndefinedLitteral()
    a2 = ALitteral(sqrt(2))
    return Addition(a1, a2)


def getAdditionOfUndefinedAndUndefined():
    a1 = UndefinedLitteral()
    a2 = UndefinedLitteral()
    return Addition(a1, a2)


def getAdditionOf10AndX():
    a1 = ALitteral(10)
    a2 = ALitteral(Variable('X'))
    return Addition(a1, a2)


def getAdditionOfXAnd20():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(20)
    return Addition(a1, a2)


def getAdditionOfABCAndX():
    a1 = ALitteral('abc')
    a2 = ALitteral(Variable('X'))
    return Addition(a1, a2)


def getAdditionOfXAndDEF():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral('def')
    return Addition(a1, a2)


def getAdditionOfPiAndX():
    a1 = ALitteral(pi)
    a2 = ALitteral(Variable('X'))
    return Addition(a1, a2)


def getAdditionOfXAndSQRT2():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(sqrt(2))
    return Addition(a1, a2)


def getAdditionOfXAndX():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(Variable('X'))
    return Addition(a1, a2)


def getAdditionOf10AndY():
    a1 = ALitteral(10)
    a2 = ALitteral(Variable('Y'))
    return Addition(a1, a2)


def getAdditionOfYAnd20():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(20)
    return Addition(a1, a2)


def getAdditionOfABCAndY():
    a1 = ALitteral('abc')
    a2 = ALitteral(Variable('Y'))
    return Addition(a1, a2)


def getAdditionOfYAndDEF():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral('def')
    return Addition(a1, a2)


def getAdditionOfPiAndY():
    a1 = ALitteral(pi)
    a2 = ALitteral(Variable('Y'))
    return Addition(a1, a2)


def getAdditionOfYAndSQRT2():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(sqrt(2))
    return Addition(a1, a2)


def getAdditionOfYAndY():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(Variable('Y'))
    return Addition(a1, a2)


def getAdditionOfXAndY():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(Variable('Y'))
    return Addition(a1, a2)


def getAdditionOfYAndX():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(Variable('X'))
    return Addition(a1, a2)


def getSubtractionOf10And20():
    a1 = ALitteral(10)
    a2 = ALitteral(20)
    return Subtraction(a1, a2)


def getSubtractionOfABCAndDEF():
    a1 = ALitteral('abc')
    a2 = ALitteral('def')
    return Subtraction(a1, a2)


def getSubtractionOfPiAndSQRT2():
    a1 = ALitteral(pi)
    a2 = ALitteral(sqrt(2))
    return Subtraction(a1, a2)


def getSubtractionOfABCAnd20():
    a1 = ALitteral('abc')
    a2 = ALitteral(20)
    return Subtraction(a1, a2)


def getSubtractionOf10AndDEF():
    a1 = ALitteral(10)
    a2 = ALitteral('def')
    return Subtraction(a1, a2)


def getSubtractionOfPiAnd20():
    a1 = ALitteral(pi)
    a2 = ALitteral(20)
    return Subtraction(a1, a2)


def getSubtractionOf10AndSQRT2():
    a1 = ALitteral(10)
    a2 = ALitteral(sqrt(2))
    return Subtraction(a1, a2)


def getSubtractionOfPiAndDEF():
    a1 = ALitteral(pi)
    a2 = ALitteral('def')
    return Subtraction(a1, a2)


def getSubtractionOfABCAndSQRT2():
    a1 = ALitteral('abc')
    a2 = ALitteral(sqrt(2))
    return Subtraction(a1, a2)


def getSubtractionOf10AndUndefined():
    a1 = ALitteral(10)
    a2 = UndefinedLitteral()
    return Subtraction(a1, a2)


def getSubtractionOfUndefinedAnd20():
    a1 = UndefinedLitteral()
    a2 = ALitteral(20)
    return Subtraction(a1, a2)


def getSubtractionOfABCAndUndefined():
    a1 = ALitteral('abc')
    a2 = UndefinedLitteral()
    return Subtraction(a1, a2)


def getSubtractionOfUndefinedAndDEF():
    a1 = UndefinedLitteral()
    a2 = ALitteral('def')
    return Subtraction(a1, a2)


def getSubtractionOfPiAndUndefined():
    a1 = ALitteral(pi)
    a2 = UndefinedLitteral()
    return Subtraction(a1, a2)


def getSubtractionOfUndefinedAndSQRT2():
    a1 = UndefinedLitteral()
    a2 = ALitteral(sqrt(2))
    return Subtraction(a1, a2)


def getSubtractionOfUndefinedAndUndefined():
    a1 = UndefinedLitteral()
    a2 = UndefinedLitteral()
    return Subtraction(a1, a2)


def getSubtractionOf10AndX():
    a1 = ALitteral(10)
    a2 = ALitteral(Variable('X'))
    return Subtraction(a1, a2)


def getSubtractionOfXAnd20():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(20)
    return Subtraction(a1, a2)


def getSubtractionOfABCAndX():
    a1 = ALitteral('abc')
    a2 = ALitteral(Variable('X'))
    return Subtraction(a1, a2)


def getSubtractionOfXAndDEF():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral('def')
    return Subtraction(a1, a2)


def getSubtractionOfPiAndX():
    a1 = ALitteral(pi)
    a2 = ALitteral(Variable('X'))
    return Subtraction(a1, a2)


def getSubtractionOfXAndSQRT2():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(sqrt(2))
    return Subtraction(a1, a2)


def getSubtractionOfXAndX():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(Variable('X'))
    return Subtraction(a1, a2)


def getSubtractionOf10AndY():
    a1 = ALitteral(10)
    a2 = ALitteral(Variable('Y'))
    return Subtraction(a1, a2)


def getSubtractionOfYAnd20():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(20)
    return Subtraction(a1, a2)


def getSubtractionOfABCAndY():
    a1 = ALitteral('abc')
    a2 = ALitteral(Variable('Y'))
    return Subtraction(a1, a2)


def getSubtractionOfYAndDEF():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral('def')
    return Subtraction(a1, a2)


def getSubtractionOfPiAndY():
    a1 = ALitteral(pi)
    a2 = ALitteral(Variable('Y'))
    return Subtraction(a1, a2)


def getSubtractionOfYAndSQRT2():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(sqrt(2))
    return Subtraction(a1, a2)


def getSubtractionOfYAndY():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(Variable('Y'))
    return Subtraction(a1, a2)


def getSubtractionOfXAndY():
    a1 = ALitteral(Variable('X'))
    a2 = ALitteral(Variable('Y'))
    return Subtraction(a1, a2)


def getSubtractionOfYAndX():
    a1 = ALitteral(Variable('Y'))
    a2 = ALitteral(Variable('X'))
    return Subtraction(a1, a2)