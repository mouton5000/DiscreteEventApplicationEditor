__author__ = 'mouton'

import pygame
from pygame.sprite import Sprite
from database import Event


_scene = None


class SpriteReg(Sprite):

    registery = ['cadre.png', 'case_02.png', 'case_04.png', 'case_08.png', 'case_16.png', 'case_32.png', 'case_64.png']

    instances = {}

    def __init__(self, name, num, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load('sprites/' + SpriteReg.registery[num]).convert_alpha(_scene)
        SpriteReg.instances[name] = self
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


_all_list = None


def init():
    global _scene, _all_list
    pygame.display.init()
    _scene = pygame.display.set_mode([800, 640])
    _scene.fill((255, 255, 255))
    _all_list = pygame.sprite.OrderedUpdates()
    _all_list.draw(_scene)
    pygame.display.flip()


_clock = pygame.time.Clock()


def tick():
    global _all_list, _clock

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Event.events.add(Event('Key', 'left'))
            if event.key == pygame.K_RIGHT:
                Event.events.add(Event('Key', 'right'))
            if event.key == pygame.K_DOWN:
                Event.events.add(Event('Key', 'down'))
            if event.key == pygame.K_UP:
                Event.events.add(Event('Key', 'up'))
    _scene.fill((255, 255, 255))
    _all_list.draw(_scene)
    pygame.display.flip()
    _clock.tick(60)

    return True


def addSprite(name, num, x, y):
    global _all_list
    _all_list.add(SpriteReg(name, num, x, y))


def removeSprite(name):
    global _all_list
    _all_list.remove(SpriteReg.instances[name])


def moveSprite(name, dx, dy):
    sp = SpriteReg.instances[name]
    sp.rect.x += dx
    sp.rect.y += dy


def editSprite(name, num):
    sp = SpriteReg.instances[name]
    x = sp.rect.x
    y = sp.rect.y
    sp.image = pygame.image.load('sprites/' + SpriteReg.registery[num]).convert_alpha(_scene)
    sp.rect = sp.image.get_rect()
    sp.rect.x = x
    sp.rect.y = y


def hide():
    global _scene
    pygame.display.quit()
    _scene = None