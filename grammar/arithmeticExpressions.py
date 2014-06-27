from database import Variable


class ALitteral(object):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def value(self, evaluation):
        try:
            return evaluation[self._value]
        except KeyError:
            pass

        if isinstance(self._value, Variable):
            raise ValueError
        else:
            return self._value


class ABiOp(object):
    def __init__(self, a1, a2):
        self._a1 = a1
        self._a2 = a2

    def __str__(self):
        return '(' + str(self._a1) + ' ' + self.symbol + ' ' + str(self._a2) + ')'

    def value(self, evaluation):
        v1 = self._a1.value(evaluation)
        v2 = self._a2.value(evaluation)
        return self.operation(v1, v2)


class Addition(ABiOp):
    def __init__(self, a1, a2):
        super(Addition, self).__init__(a1, a2)
        self.symbol = '+'

    def operation(self, v1, v2):
        try:
            return v1 + v2
        except TypeError:
            return str(v1) + str(v2)


class Subtraction(ABiOp):
    def __init__(self, a1, a2):
        super(Subtraction, self).__init__(a1, a2)
        self.symbol = '-'

    def operation(self, v1, v2):
        return v1 - v2


class Product(ABiOp):
    def __init__(self, a1, a2):
        super(Product, self).__init__(a1, a2)
        self.symbol = '*'

    def operation(self, v1, v2):
        return v1 * v2


class Division(ABiOp):
    def __init__(self, a1, a2):
        super(Division, self).__init__(a1, a2)
        self.symbol = '/'

    def operation(self, v1, v2):
        return float(v1) / float(v2)


class EuclideanDivision(ABiOp):
    def __init__(self, a1, a2):
        super(EuclideanDivision, self).__init__(a1, a2)
        self.symbol = '//'

    def operation(self, v1, v2):
        return v1 // v2


class Modulo(ABiOp):
    def __init__(self, a1, a2):
        super(Modulo, self).__init__(a1, a2)
        self.symbol = '%'

    def operation(self, v1, v2):
        return v1 % v2


class Power(ABiOp):
    def __init__(self, a1, a2):
        super(Power, self).__init__(a1, a2)
        self.symbol = '**'

    def operation(self, v1, v2):
        return v1 ** v2


class AUnOp(object):
    def __init__(self, a):
        self._a = a

    def __str__(self):
        return self._symbol + '('  + str(self._a) + ')'

    def value(self, evaluation):
        v = self._a.value(evaluation)
        return self.operation(v)


class Func(AUnOp):
    def __init__(self, a, func):
        super(Func, self).__init__(a)
        self._func = func
        self._symbol = str(func)[19:-1]

    def operation(self, v):
        return self._func(v)