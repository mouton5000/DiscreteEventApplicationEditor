__author__ = 'mouton'

from pygame.sprite import Sprite
import pygame
from database import UNDEFINED_PARAMETER


_spriteRegs = {}
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

    def __init__(self, num, filePath, x, y, scene):
        Sprite.__init__(self)
        self.num = None
        self.reload(num, filePath, x, y, scene)

    def reload(self, num, filePath, x, y, scene):
        if self.num is None or self.num != num:
            self.num = num
            self.image = pygame.image.load(filePath).convert_alpha(scene)
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return str((self.num, self.rect))

    def __repr__(self):
        return str((self.num, self.rect))


def addSprite(name, num, x, y):
    try:
        filePath = _rootDir + '/' + _spritesDictionnary[num]
        import game.gameWindow as gameWindow
        scene = gameWindow.getScene()
        sp = SpriteReg(num, filePath, x, y, scene)
        spritesList.add(sp)
        _spriteRegs[name] = sp
    except KeyError:
        pass


def removeSprite(name):
    try:
        spritesList.remove(_spriteRegs[name])
    except KeyError:
        pass


def editSprite(name, unevaluatedNum, unevaluatedX, unevaluatedY, evaluation):
    try:
        sp = _spriteRegs[name]
    except KeyError:
        return
    newNum = unevaluatedNum.value(evaluation, selfParam=sp.num)
    if newNum == UNDEFINED_PARAMETER:
        newNum = sp.num
    else:
        newNum = int(newNum)

    x = sp.rect.x
    y = sp.rect.y
    newX = unevaluatedX.value(evaluation, selfParam=x)
    if newX == UNDEFINED_PARAMETER:
        newX = x
    else:
        newX = int(newX)
    newY = unevaluatedY.value(evaluation, selfParam=y)
    if newY == UNDEFINED_PARAMETER:
        newY = y
    else:
        newY = int(newY)

    try:
        newFilePath = _rootDir + '/' + _spritesDictionnary[newNum]
        import game.gameWindow as gameWindow
        scene = gameWindow.getScene()
        sp.reload(newNum, newFilePath, newX, newY, scene)
    except KeyError:
        pass