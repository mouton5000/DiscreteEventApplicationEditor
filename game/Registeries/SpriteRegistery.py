__author__ = 'mouton'

from pygame.sprite import Sprite
import pygame
from collections import defaultdict

_rootDir = None

_spritesList = defaultdict(pygame.sprite.OrderedUpdates)


def init(rootDir):
    global _rootDir
    _rootDir = rootDir
    reinit()


def reinit():
    _spritesList.clear()


def getLayers():
    return iter(_spritesList.keys())


def draw(z, scene):
    _spritesList[z].draw(scene)


class SpriteReg(Sprite):

    def __init__(self, fileName, x, y, z, rotate, scale):
        Sprite.__init__(self)
        self.fileName = None
        self.z = None
        self.reload(fileName, x, y, z, rotate, scale)

    def reload(self, fileName, x, y, z, rotate, scale):
        filePath = _rootDir + '/' + fileName
        import game.gameWindow as gameWindow
        scene = gameWindow.getScene()

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