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

        try:
            if self._value[0].isupper():
                return None
        except TypeError:
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