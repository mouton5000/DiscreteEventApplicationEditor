__author__ = 'mouton'

import pygame
from pygame.sprite import Sprite
from database import Event, UNDEFINED_PARAMETER


class SpriteReg(Sprite):

    instances = {}

    def __init__(self, name, num, filePath, x, y, scene):
        Sprite.__init__(self)
        self.name = name
        SpriteReg.instances[name] = self
        self.num = None
        self.reload(num, filePath, x, y, scene)

    def reload(self, num, filePath, x, y, scene):
        if self.num is None or self.num != num:
            self.num = num
            self.image = pygame.image.load(filePath).convert_alpha(scene)
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class GameWindow:

    def __init__(self, fps, width, height, spritesRegistery):
        pygame.init()
        pygame.display.init()
        self._scene = pygame.display.set_mode([width, height])
        self._scene.fill((255, 255, 255))
        self._spritesList = pygame.sprite.OrderedUpdates()
        self._spritesList.draw(self._scene)
        self._fps = fps
        self._spriteRegistery = spritesRegistery
        pygame.display.flip()
        self._clock = pygame.time.Clock()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Event.events.add(Event('Key', ['left']))
                if event.key == pygame.K_RIGHT:
                    Event.events.add(Event('Key', ['right']))
                if event.key == pygame.K_DOWN:
                    Event.events.add(Event('Key', ['down']))
                if event.key == pygame.K_UP:
                    Event.events.add(Event('Key', ['up']))
        self._scene.fill((255, 255, 255))
        self._spritesList.draw(self._scene)

        pygame.display.flip()

        self._clock.tick(self._fps)

        return True

    def addSprite(self, name, num, x, y):
        try:
            filePath = self._spriteRegistery[num]
            self._spritesList.add(SpriteReg(name, num, filePath, x, y, self._scene))
        except KeyError:
            pass

    def removeSprite(self, name):
        try:
            self._spritesList.remove(SpriteReg.instances[name])
        except KeyError:
            pass

    def editSprite(self, name, unevaluatedNum, unevaluatedX, unevaluatedY, evaluation):
        try:
            sp = SpriteReg.instances[name]
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
            newFilePath = self._spriteRegistery[newNum]
            sp.reload(newNum, newFilePath, newX, newY, self._scene)
        except KeyError:
            pass

    def hide(self):
        pygame.display.quit()
        self._scene = None