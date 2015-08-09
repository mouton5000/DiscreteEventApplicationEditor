__author__ = 'mouton'

import pygame

from database import Event
import game.Registeries.SoundRegistery as soundReg
import game.Registeries.SpriteRegistery as spriteReg
import game.Registeries.TextRegistery as textReg
import game.Registeries.LineRegistery as lineReg
import game.Registeries.RectRegistery as rectReg
import game.Registeries.OvalRegistery as ovalReg
import game.Registeries.PolygonRegistery as polygonReg

from itertools import chain

pygame.init()
pygame.display.init()
pygame.joystick.init()
pygame.mixer.init()
pygame.font.init()

_scene = None

_fps = 0
_width = 0
_height = 0

_clock = pygame.time.Clock()


def init(fps, width, height, soundsDictionnary, rootDir):
    global _scene, _fps, _width, _height
    _scene = pygame.display.set_mode([width, height])
    _scene.fill((255, 255, 255))
    _fps = fps
    _width = width
    _height = height
    spriteReg.init(rootDir)
    soundReg.init(soundsDictionnary, rootDir)

    textReg.init(rootDir)
    lineReg.init()
    rectReg.init()
    ovalReg.init()
    polygonReg.init()

    pygame.display.flip()


def reinit():
    spriteReg.reinit()
    textReg.reinit()
    lineReg.reinit()
    rectReg.reinit()
    ovalReg.reinit()
    polygonReg.reinit()
    soundReg.reinit()


def tick():
    if not _readEvents():
        return False

    _scene.fill((255, 255, 255))

    regs = [spriteReg, lineReg, ovalReg, rectReg, polygonReg, textReg]

    # Il est necessaire de passer par cette fonction auxilliaire, sinon c'est le meme code qui est attribue a tous
    # les generateurs
    def _getLayersTuple(code, reg):
        return ((layer, code) for layer in reg.getLayers())
    layers = chain(*(_getLayersTuple(code, reg) for code, reg in enumerate(regs)))

    layers = sorted(layers)

    for layer, code in layers:
        regs[code].draw(layer, _scene)

    pygame.display.flip()

    _clock.tick(_fps)

    return True


def getScene():
    return _scene


def hide():
    global _scene
    pygame.display.quit()
    _scene = None


def getFps():
    return _fps


def setFps(fps):
    global _fps
    _fps = fps


def getWidth():
    return _width


def setWidth(width):
    global _width, _scene
    _width = width
    _scene = pygame.display.set_mode([width, _height])  # Meilleur moyen?


def getHeight():
    return _height


def setHeight(height):
    global _height, _scene
    _height = height
    _scene = pygame.display.set_mode([_width, height])  # Meilleur moyen?


def _readEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            _readKeyDownEvent(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            _readMouseButtonUpEvent(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            _readMouseButtonDownEvent(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            _readJoystickButtonDownEvent(event)
        elif event.type == pygame.JOYAXISMOTION:
            _readJoystickAxisMotionEvent(event)
        elif event.type == pygame.JOYHATMOTION:
            _readJoystickHatMotionEvent(event)
        elif event.type == pygame.JOYBALLMOTION:
            _readJoystickBallMotionEvent(event)
    return True


def _readKeyDownEvent(event):
    if event.key == pygame.K_LEFT:
        Event.add('Key', ['left'], {})
    elif event.key == pygame.K_RIGHT:
        Event.add('Key', ['right'], {})
    elif event.key == pygame.K_DOWN:
        Event.add('Key', ['down'], {})
    elif event.key == pygame.K_UP:
        Event.add('Key', ['up'], {})


def _readMouseButtonUpEvent(event):
    Event.add('MouseUp', [event.pos[0], event.pos[1]], {})


def _readMouseButtonDownEvent(event):
    Event.add('Mouse', [event.pos[0], event.pos[1]], {})


def _readJoystickButtonDownEvent(event):
    Event.add('JoystickButton', [event.joy, event.button], {})


def _readJoystickAxisMotionEvent(event):
    Event.add('JoystickAxisMotion', [event.joy, event.axis, event.pos[0], event.pos[1]], {})


def _readJoystickHatMotionEvent(event):
    Event.add('JoystickHatMotion', [event.joy, event.hat, event.pos[0], event.pos[1]], {})


def _readJoystickBallMotionEvent(event):
    Event.add('JoystickBallMotion', [event.joy, event.ball, event.rel[0], event.rel[1]], {})