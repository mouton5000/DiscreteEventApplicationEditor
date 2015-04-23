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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Event.add('Key', ['left'], {})
            if event.key == pygame.K_RIGHT:
                Event.add('Key', ['right'], {})
            if event.key == pygame.K_DOWN:
                Event.add('Key', ['down'], {})
            if event.key == pygame.K_UP:
                Event.add('Key', ['up'], {})
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Event.add('Mouse', [event.pos[0], event.pos[1]], {})
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


def getWidth():
    return _width


def getHeight():
    return _height