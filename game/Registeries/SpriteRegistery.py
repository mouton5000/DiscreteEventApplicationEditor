__author__ = 'mouton'

from pygame.sprite import Sprite
import pygame


_spritesDictionnary = None
_rootDir = None

spritesList = pygame.sprite.OrderedUpdates()


def init(spritesDictionnary, rootDir):
    global _spritesDictionnary, _rootDir
    _spritesDictionnary = spritesDictionnary
    _rootDir = rootDir
    reinit()


def reinit():
    spritesList.empty()


class SpriteReg(Sprite):

    def __init__(self, code, x, y):
        Sprite.__init__(self)
        self.num = None
        self.reload(code, x, y)
        spritesList.add(self)

    def reload(self, code, x, y):
        filePath = _rootDir + '/' + _spritesDictionnary[code]
        import game.gameWindow as gameWindow
        scene = gameWindow.getScene()

        if self.num is None or self.num != code:
            self.num = code
            self.image = pygame.image.load(filePath).convert_alpha(scene)
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return str((self.num, self.rect))

    def __repr__(self):
        return str((self.num, self.rect))

    def remove(self):
        spritesList.remove(self)