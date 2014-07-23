from database import Property, Event
import game.gameWindow as gameWindow

__author__ = 'mouton'


def _evalArg(arg, evaluation):
    return arg.value(evaluation)


class AddPropertyConsequence():

    def __init__(self, name, args):
        self._name = name
        self._args = args

    def eval_update(self, evaluation, *_):
        try:
            name = self._name
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            prop = Property(name, newArgs)
            Property.properties.add(prop)
            return name, newArgs
        except (ArithmeticError, TypeError, ValueError):
            pass


class RemovePropertyConsequence():

    def __init__(self, name, args):
        self._name = name
        self._args = args

    def eval_update(self, evaluation, *_):
        try:
            name = self._name
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            Property.removeAll(name, newArgs)
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditPropertyConsequence():

    def __init__(self, name, args1, args2):
        self._name = name
        self._args1 = args1
        self._args2 = args2

    def eval_update(self, evaluation, *_):
        try:
            name = self._name
            newArgs1 = [_evalArg(arg, evaluation) for arg in self._args1]
            Property.edit(name, newArgs1, self._args2, evaluation)
        except (ArithmeticError, TypeError, ValueError):
            pass


class AddEventConsequence():
    events = set([])

    def __init__(self, name, args):
        self._name = name
        self._args = args

    def eval_update(self, evaluation, *_):
        try:
            name = self._name
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            event = Event(name, newArgs)
            Event.events.add(event)
        except (ArithmeticError, TypeError, ValueError):
            pass


class SpriteConsequence(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class AddSpriteConsequence(SpriteConsequence):
    def __init__(self, name, num, x, y):
        super(AddSpriteConsequence, self).__init__(name)
        self._num = num
        self._x = x
        self._y = y

    def eval_update(self, evaluation, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            num = int(_evalArg(self._num, evaluation))
            x = int(_evalArg(self._x, evaluation))
            y = int(_evalArg(self._y, evaluation))
            gameWindow.addSprite(name, num, x, y)
        except (ArithmeticError, TypeError, ValueError):
            pass

    @property
    def num(self):
        return self._num

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class RemoveSpriteConsequence(SpriteConsequence):
    def __init__(self, name):
        super(RemoveSpriteConsequence, self).__init__(name)

    def eval_update(self, evaluation, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            try:
                gameWindow.removeSprite(name)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditSpriteConsequence(SpriteConsequence):
    def __init__(self, name, num, x, y):
        super(EditSpriteConsequence, self).__init__(name)
        self._num = num
        self._x = x
        self._y = y

    def eval_update(self, evaluation, *_):
        try:
            name = _evalArg(self._name, evaluation)
            try:
                gameWindow.editSprite(name, self._num, self._x, self._y, evaluation)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass

    @property
    def num(self):
        return self._num


class AddTokenConsequence(object):
    def __init__(self, nodeNum, args):
        self._nodeNum = nodeNum
        self._parameters = args

    @property
    def nodeNum(self):
        return self._nodeNum

    @property
    def parameters(self):
        return self._parameters

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            nodeNum = int(_evalArg(self._nodeNum, evaluation))
            newParameters = [_evalArg(arg, evaluation) for arg in self._parameters]
            stateMachine.addTokenByNodeNum(nodeNum, newParameters)
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditTokenConsequence(object):
    def __init__(self, args):
        self._parameters = args

    @property
    def parameters(self):
        return self._parameters

    def eval_update(self, evaluation, _, token):
        try:
            token.setArgs(self._parameters, evaluation)
        except (ArithmeticError, TypeError, ValueError):
            pass


class RemoveTokenConsequence(object):
    def __init__(self):
        pass

    def eval_update(self, _, stateMachine, token):
        stateMachine.removeToken(token)