__author__ = 'mouton'

import pygame
from pygame import Color
from pygame.rect import Rect

from database import Event
import game.Registeries.SpriteRegistery as spriteReg
import game.Registeries.TextRegistery as textReg
import game.Registeries.LineRegistery as lineReg
import game.Registeries.RectRegistery as rectReg
import game.Registeries.OvalRegistery as ovalReg
import game.Registeries.PolygonRegistery as polygonReg

pygame.init()
pygame.display.init()
pygame.joystick.init()


_scene = None

_fps = 0
_width = 0
_height = 0

_clock = pygame.time.Clock()


def init(fps, width, height, spritesDictionnary, rootDir):
    global _scene, _fps, _width, _height
    _scene = pygame.display.set_mode([width, height])
    _scene.fill((255, 255, 255))
    _fps = fps
    _width = width
    _height = height
    spriteReg.init(spritesDictionnary, rootDir)
    spriteReg.spritesList.draw(_scene)

    textReg.init()
    lineReg.init()
    rectReg.init()
    ovalReg.init()
    polygonReg.init()

    pygame.display.flip()


def tick():
    if not _readEvents():
        return False

    _scene.fill((255, 255, 255))

    for lineItem in lineReg.lineItemsIterator():
        color = Color('#' + lineItem.colorName)
        pygame.draw.line(_scene, color, (lineItem.x1, lineItem.y1), (lineItem.x2, lineItem.y2), lineItem.width)

    for rectItem in rectReg.rectItemsIterator():
        color = Color('#' + rectItem.colorName)
        pygame.draw.rect(_scene, color, Rect(rectItem.x, rectItem.y, rectItem.w, rectItem.h), rectItem.width)

    for ovalItem in ovalReg.ovalItemsIterator():
        color = Color('#' + ovalItem.colorName)
        pygame.draw.ellipse(_scene, color, Rect(ovalItem.x - ovalItem.a, ovalItem.y - ovalItem.b,
                                                     2 * ovalItem.a, 2 * ovalItem.b), ovalItem.width)

    for polygonItem in polygonReg.polygonItemsIterator():
        color = Color('#' + polygonItem.colorName)
        pygame.draw.polygon(_scene, color, polygonItem.pointList, polygonItem.width)

    spriteReg.spritesList.draw(_scene)

    for textItem in textReg.textItemsIterator():
        label = textItem.label
        textPos = label.get_rect()
        textPos.centerx = textItem.x
        textPos.centery = textItem.y
        _scene.blit(label, textPos)

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