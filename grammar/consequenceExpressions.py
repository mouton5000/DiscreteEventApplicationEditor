__author__ = 'mouton'

from database import Property, Event, SpriteProperty, LineProperty, \
    OvalProperty, RectProperty, TextProperty, PolygonProperty
import stateMachine
import game.Registeries.SoundRegistery as soundRegistery
import game.gameWindow as gameWindow


def _evalArg(arg, evaluation):
    return arg.value(evaluation)


class NamedConsequence(object):
    def __init__(self, name):
        self._name = name


class AddParameterizedNamedConsequence(object):

    def __init__(self, name, args, kwargs):
        self._name = name
        self._args = args
        self._kwargs = kwargs

    def _eval_args(self, cls, evaluation):
        try:
            name = self._name
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            newKWargs = {_evalArg(key, evaluation): _evalArg(value, evaluation)
                         for key, value in self._kwargs.iteritems()}
            cls.add(name, newArgs, newKWargs)
            return name, newArgs, newKWargs
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class RemoveParameterizedNamedConsequence(object):

    def __init__(self, name, args, kwargs):
        self._name = name
        self._args = args
        self._kwargs = kwargs

    def _eval_args(self, cls, evaluation):
        try:
            name = self._name
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            newKWargs = {_evalArg(key, evaluation): _evalArg(value, evaluation)
                         for key, value in self._kwargs.iteritems()}
            cls.removeAll(name, newArgs, newKWargs)
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class EditParameterizedNamedConsequence(object):

    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        self._name = name
        self._args1 = args1
        self._kwargs1 = kwargs1
        self._args2 = args2
        self._kwargs2 = kwargs2

    def _eval_args(self, cls, evaluation):
        try:
            name = self._name
            newArgs1 = [_evalArg(arg, evaluation) for arg in self._args1]
            newKWArgs1 = {_evalArg(key, evaluation): _evalArg(value, evaluation)
                          for key, value in self._kwargs1.iteritems()}
            cls.editAll(name, newArgs1, newKWArgs1, self._args2, self._kwargs2, evaluation)
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class AddPropertyConsequence(AddParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(AddPropertyConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(Property, evaluation)


class RemovePropertyConsequence(RemoveParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(RemovePropertyConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(Property, evaluation)


class EditPropertyConsequence(EditParameterizedNamedConsequence):

    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        super(EditPropertyConsequence, self).__init__(name, args1, kwargs1, args2, kwargs2)

    def eval_update(self, evaluation, *_):
        self._eval_args(Property, evaluation)


class AddEventConsequence(AddParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(AddEventConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(Event, evaluation)


class AddSpriteConsequence(AddParameterizedNamedConsequence):
    def __init__(self, name, args, kwargs):
        super(AddSpriteConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(SpriteProperty, evaluation)


class RemoveSpriteConsequence(RemoveParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(RemoveSpriteConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(SpriteProperty, evaluation)


class EditSpriteConsequence(EditParameterizedNamedConsequence):

    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        super(EditSpriteConsequence, self).__init__(name, args1, kwargs1, args2, kwargs2)

    def eval_update(self, evaluation, *_):
        self._eval_args(SpriteProperty, evaluation)


class AddTextConsequence(AddParameterizedNamedConsequence):
    def __init__(self, name, args, kwargs):
        super(AddTextConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(TextProperty, evaluation)


class RemoveTextConsequence(RemoveParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(RemoveTextConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(TextProperty, evaluation)


class EditTextConsequence(EditParameterizedNamedConsequence):

    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        super(EditTextConsequence, self).__init__(name, args1, kwargs1, args2, kwargs2)

    def eval_update(self, evaluation, *_):
        self._eval_args(TextProperty, evaluation)


class AddLineConsequence(AddParameterizedNamedConsequence):
    def __init__(self, name, args, kwargs):
        super(AddLineConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(LineProperty, evaluation)


class RemoveLineConsequence(RemoveParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(RemoveLineConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(LineProperty, evaluation)


class EditLineConsequence(EditParameterizedNamedConsequence):

    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        super(EditLineConsequence, self).__init__(name, args1, kwargs1, args2, kwargs2)

    def eval_update(self, evaluation, *_):
        self._eval_args(LineProperty, evaluation)


class AddOvalConsequence(AddParameterizedNamedConsequence):
    def __init__(self, name, args, kwargs):
        super(AddOvalConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(OvalProperty, evaluation)


class RemoveOvalConsequence(RemoveParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(RemoveOvalConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(OvalProperty, evaluation)


class EditOvalConsequence(EditParameterizedNamedConsequence):

    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        super(EditOvalConsequence, self).__init__(name, args1, kwargs1, args2, kwargs2)

    def eval_update(self, evaluation, *_):
        self._eval_args(OvalProperty, evaluation)


class AddRectConsequence(AddParameterizedNamedConsequence):
    def __init__(self, name, args, kwargs):
        super(AddRectConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(RectProperty, evaluation)


class RemoveRectConsequence(RemoveParameterizedNamedConsequence):

    def __init__(self, name, args, kwargs):
        super(RemoveRectConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(RectProperty, evaluation)


class EditRectConsequence(EditParameterizedNamedConsequence):
    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        super(EditRectConsequence, self).__init__(name, args1, kwargs1, args2, kwargs2)

    def eval_update(self, evaluation, *_):
        self._eval_args(RectProperty, evaluation)


class AddPolygonConsequence(AddParameterizedNamedConsequence):
    def __init__(self, name, args, kwargs):
        super(AddPolygonConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(PolygonProperty, evaluation)


class RemovePolygonConsequence(RemoveParameterizedNamedConsequence):
    def __init__(self, name, args, kwargs):
        super(RemovePolygonConsequence, self).__init__(name, args, kwargs)

    def eval_update(self, evaluation, *_):
        self._eval_args(PolygonProperty, evaluation)


class EditPolygonConsequence(EditParameterizedNamedConsequence):
    def __init__(self, name, args1, kwargs1, args2, kwargs2):
        super(EditPolygonConsequence, self).__init__(name, args1, kwargs1, args2, kwargs2)

    def eval_update(self, evaluation, *_):
        self._eval_args(PolygonProperty, evaluation)


class AddTokenConsequence(object):
    def __init__(self, nodeNum, args, kwargs):
        self._nodeNum = nodeNum
        self._args = args
        self._kwargs = kwargs

    def eval_update(self, evaluation, *_):
        try:
            nodeNum = int(_evalArg(self._nodeNum, evaluation))
            newArgs = [_evalArg(arg, evaluation) for arg in self._args]
            newKWArgs = {_evalArg(key, evaluation): _evalArg(value, evaluation)
                         for key, value in self._kwargs.iteritems()}
            stateMachine.addTokenByNodeNum(nodeNum, newArgs, newKWArgs)
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditTokenConsequence(object):
    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs

    def eval_update(self, evaluation, token):
        try:
            token.setArgs(self._args, self._kwargs, evaluation)
        except (ArithmeticError, TypeError, ValueError):
            pass


class RemoveTokenConsequence(object):
    def __init__(self):
        pass

    def eval_update(self, _, token):
        stateMachine.removeToken(token)


class RemoveAllTokenConsequence(object):
    def __init__(self):
        pass

    def eval_update(self, *_):
        stateMachine.removeAllToken()


class PrintConsequence(object):
    def __init__(self, toPrint):
        self.toPrint = toPrint

    def eval_update(self, evaluation, *_):
        try:
            print ' '.join(str(_evalArg(foo, evaluation)) for foo in self.toPrint)
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditGlobalFps(object):
    def __init__(self, newValue):
        self.newValue = newValue

    def eval_update(self, evaluation, *_):
        fps = _evalArg(self.newValue, evaluation)
        gameWindow.setFps(fps)


class EditGlobalWidth(object):
    def __init__(self, newValue):
        self.newValue = newValue

    def eval_update(self, evaluation, *_):
        width = _evalArg(self.newValue, evaluation)
        gameWindow.setWidth(width)


class EditGlobalHeight(object):
    def __init__(self, newValue):
        self.newValue = newValue

    def eval_update(self, evaluation, *_):
        height = _evalArg(self.newValue, evaluation)
        gameWindow.setHeight(height)


class ClearAll(object):
    def __init__(self):
        pass

    def eval_update(self, evaluation, *_):
        stateMachine.reinit()
        gameWindow.reinit()


class AddSoundConsequence():
    def __init__(self, num):
        self._num = num

    def eval_update(self, evaluation, *_):
        try:
            num = int(_evalArg(self._num, evaluation))
            soundRegistery.playSound(num)
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