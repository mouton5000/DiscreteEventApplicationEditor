from pygame.rect import Rect

__author__ = 'mouton'

from pygame.sprite import Sprite
import pygame
from collections import defaultdict
from copy import copy

_rootDir = None

_spritesList = defaultdict(pygame.sprite.OrderedUpdates)
_rectsToUpdate = []


def init(rootDir):
    global _rootDir
    _rootDir = rootDir
    reinit()


def reinit():
    _spritesList.clear()
    del _rectsToUpdate[:]


def getLayers():
    return iter(_spritesList.keys())


def draw(z, scene):
    _spritesList[z].draw(scene)


def addRectToUpdate(rectToUpdate):
    _rectsToUpdate.append(rectToUpdate)


def getRectsToUpdate():
    return _rectsToUpdate


def clearRectsToUpdate():
    del _rectsToUpdate[:]


class SpriteReg(Sprite):

    def __init__(self, fileName, x, y, z, rotate, scale):
        Sprite.__init__(self)
        self.fileName = None
        self.z = None
        self.rect = None
        self.reload(fileName, x, y, z, rotate, scale)

    def reload(self, fileName, x, y, z, rotate, scale):
        filePath = _rootDir + '/' + fileName
        import game.gameWindow as gameWindow
        scene = gameWindow.getScene()

        prevRect = copy(self.rect)

        if self.fileName is None or self.fileName != fileName or rotate != 0 or scale != 1:
            self.fileName = fileName
            self.image = pygame.image.load(filePath).convert_alpha(scene)
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if rotate != 0 or scale != 1:
            self.image = pygame.transform.rotozoom(self.image, rotate, scale)
            transformedRect = self.image.get_rect()
            transformedRect.center = self.rect.center
            self.rect = transformedRect

        if prevRect is not None:

            rectToUpdate = Rect(prevRect.x - 1, prevRect.y - 1, prevRect.width + 2, prevRect.height + 2)
            r2 = Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
            rectToUpdate.union_ip(r2)
            addRectToUpdate(rectToUpdate)
        else:
            rectToUpdate = Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
            addRectToUpdate(rectToUpdate)

        if self.z is not None:
            self.remove()
        _spritesList[z].add(self)
        self.z = z

    def __str__(self):
        return str((self.fileName, self.rect))

    def __repr__(self):
        return str((self.fileName, self.rect))

    def remove(self):
        _spritesList[self.z].remove(self)
        rectToUpdate = Rect(self.rect.x - 1, self.rect.y - 1, self.rect.width + 2, self.rect.height + 2)
        addRectToUpdate(rectToUpdate)