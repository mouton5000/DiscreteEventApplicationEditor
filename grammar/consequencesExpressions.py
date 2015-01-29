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


class NamedConsequence(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class AddSpriteConsequence(NamedConsequence):
    def __init__(self, name, num, x, y):
        super(AddSpriteConsequence, self).__init__(name)
        self._num = num
        self._x = x
        self._y = y

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            num = int(_evalArg(self._num, evaluation))
            x = int(_evalArg(self._x, evaluation))
            y = int(_evalArg(self._y, evaluation))
            stateMachine.gameWindow.addSprite(name, num, x, y)
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


class RemoveSpriteConsequence(NamedConsequence):
    def __init__(self, name):
        super(RemoveSpriteConsequence, self).__init__(name)

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            try:
                stateMachine.gameWindow.removeSprite(name)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditSpriteConsequence(NamedConsequence):
    def __init__(self, name, num, x, y):
        super(EditSpriteConsequence, self).__init__(name)
        self._num = num
        self._x = x
        self._y = y

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = _evalArg(self._name, evaluation)
            try:
                stateMachine.gameWindow.editSprite(name, self._num, self._x, self._y, evaluation)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass

    @property
    def num(self):
        return self._num


class AddTextConsequence(NamedConsequence):
    def __init__(self, name, text, x, y, colorName, font, fontSize):
        super(AddTextConsequence, self).__init__(name)
        self._text = text
        self._x = x
        self._y = y
        self._colorName = colorName
        self._font = font
        self._fontSize = fontSize

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            text = str(_evalArg(self._text, evaluation))
            x = int(_evalArg(self._x, evaluation))
            y = int(_evalArg(self._y, evaluation))
            colorName = str(_evalArg(self._colorName, evaluation))
            font = str(_evalArg(self._font, evaluation))
            fontSize = int(_evalArg(self._fontSize, evaluation))
            stateMachine.gameWindow.addText(name, text, x, y, colorName, font, fontSize)
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class RemoveTextConsequence(NamedConsequence):
    def __init__(self, name):
        super(RemoveTextConsequence, self).__init__(name)

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            try:
                stateMachine.gameWindow.removeText(name)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditTextConsequence(NamedConsequence):
    def __init__(self, name, text, x, y, colorName, font, fontSize):
        super(EditTextConsequence, self).__init__(name)
        self._text = text
        self._x = x
        self._y = y
        self._colorName = colorName
        self._font = font
        self._fontSize = fontSize

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = _evalArg(self._name, evaluation)
            try:
                stateMachine.gameWindow.editText(name, self._text, self._x, self._y, self._colorName,
                                                 self._font, self._fontSize, evaluation)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class AddLineConsequence(NamedConsequence):
    def __init__(self, name, x1, y1, x2, y2, width, colorName):
        super(AddLineConsequence, self).__init__(name)
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            x1 = int(_evalArg(self._x1, evaluation))
            y1 = int(_evalArg(self._y1, evaluation))
            x2 = int(_evalArg(self._x2, evaluation))
            y2 = int(_evalArg(self._y2, evaluation))
            width = int(_evalArg(self._width, evaluation))
            colorName = str(_evalArg(self._colorName, evaluation))
            stateMachine.gameWindow.addLine(name, x1, y1, x2, y2, width, colorName)
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class RemoveLineConsequence(NamedConsequence):
    def __init__(self, name):
        super(RemoveLineConsequence, self).__init__(name)

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            try:
                stateMachine.gameWindow.removeLine(name)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditLineConsequence(NamedConsequence):
    def __init__(self, name, x1, y1, x2, y2, width, colorName):
        super(EditLineConsequence, self).__init__(name)
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = _evalArg(self._name, evaluation)
            try:
                stateMachine.gameWindow.editLine(name, self._x1, self._y1, self._x2, self._y2, self._width,
                                                 self._colorName, evaluation)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class AddRectConsequence(NamedConsequence):
    def __init__(self, name, x, y, w, h, width, colorName):
        super(AddRectConsequence, self).__init__(name)
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            x = int(_evalArg(self._x, evaluation))
            y = int(_evalArg(self._y, evaluation))
            w = int(_evalArg(self._w, evaluation))
            h = int(_evalArg(self._h, evaluation))
            width = int(_evalArg(self._width, evaluation))
            colorName = str(_evalArg(self._colorName, evaluation))
            stateMachine.gameWindow.addRect(name, x, y, w, h, width, colorName)
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class RemoveRectConsequence(NamedConsequence):
    def __init__(self, name):
        super(RemoveRectConsequence, self).__init__(name)

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            try:
                stateMachine.gameWindow.removeRect(name)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditRectConsequence(NamedConsequence):
    def __init__(self, name, x, y, w, h, width, colorName):
        super(EditRectConsequence, self).__init__(name)
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = _evalArg(self._name, evaluation)
            try:
                stateMachine.gameWindow.editRect(name, self._x, self._y, self._w, self._h, self._width,
                                                 self._colorName, evaluation)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class AddOvalConsequence(NamedConsequence):
    def __init__(self, name, x, y, a, b, width, colorName):
        super(AddOvalConsequence, self).__init__(name)
        self._x = x
        self._y = y
        self._a = a
        self._b = b
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            x = int(_evalArg(self._x, evaluation))
            y = int(_evalArg(self._y, evaluation))
            a = int(_evalArg(self._a, evaluation))
            b = int(_evalArg(self._b, evaluation))
            width = int(_evalArg(self._width, evaluation))
            colorName = str(_evalArg(self._colorName, evaluation))
            stateMachine.gameWindow.addOval(name, x, y, a, b, width, colorName)
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class RemoveOvalConsequence(NamedConsequence):
    def __init__(self, name):
        super(RemoveOvalConsequence, self).__init__(name)

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            try:
                stateMachine.gameWindow.removeOval(name)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditOvalConsequence(NamedConsequence):
    def __init__(self, name, x, y, a, b, width, colorName):
        super(EditOvalConsequence, self).__init__(name)
        self._x = x
        self._y = y
        self._b = a
        self._a = b
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = _evalArg(self._name, evaluation)
            try:
                stateMachine.gameWindow.editOval(name, self._x, self._y, self._a, self._b, self._width,
                                                 self._colorName, evaluation)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class AddPolygonConsequence(NamedConsequence):
    def __init__(self, name, listPoint, width, colorName):
        super(AddPolygonConsequence, self).__init__(name)
        self._listPoint = listPoint
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))

            def addPoint(point):
                xPoint = int(_evalArg(point[0], evaluation))
                yPoint = int(_evalArg(point[1], evaluation))
                return xPoint, yPoint

            listPoint = [addPoint(point) for point in self._listPoint]
            width = int(_evalArg(self._width, evaluation))
            colorName = str(_evalArg(self._colorName, evaluation))
            stateMachine.gameWindow.addPolygon(name, listPoint, width, colorName)
        except (ArithmeticError, TypeError, ValueError):
            import traceback
            print traceback.format_exc()


class RemovePolygonConsequence(NamedConsequence):
    def __init__(self, name):
        super(RemovePolygonConsequence, self).__init__(name)

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = str(_evalArg(self._name, evaluation))
            try:
                stateMachine.gameWindow.removePolygon(name)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


class EditPolygonConsequence(NamedConsequence):
    def __init__(self, name, listPoint, width, colorName):
        super(EditPolygonConsequence, self).__init__(name)
        self._listPoint = listPoint
        self._colorName = colorName
        self._width = width

    def eval_update(self, evaluation, stateMachine, *_):
        try:
            name = _evalArg(self._name, evaluation)
            try:
                stateMachine.gameWindow.editPolygon(name, self._listPoint, self._width,
                                                    self._colorName, evaluation)
            except KeyError:
                pass
        except (ArithmeticError, TypeError, ValueError):
            pass


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