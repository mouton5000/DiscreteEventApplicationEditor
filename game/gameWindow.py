__author__ = 'mouton'

import pygame
from pygame import Color
from pygame.sprite import Sprite
from database import Event, UNDEFINED_PARAMETER


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


class TextReg:

    def __init__(self, text, x, y, colorName, fontName, fontSize):
        self.reload(text, x, y, colorName, fontName, fontSize)

    def reload(self, text, x, y, colorName, fontName, fontSize):
        self.text = text
        self.colorName = colorName
        self.fontName = fontName
        self.fontSize = fontSize
        self.x = x
        self.y = y
        labelFont = pygame.font.SysFont(fontName, fontSize)
        self.label = labelFont.render(text, True, Color('#' + self.colorName))


class GameWindow:
    def __init__(self, fps, width, height, spritesRegistery, rootDir):
        pygame.init()
        pygame.display.init()
        self._scene = pygame.display.set_mode([width, height])
        self._scene.fill((255, 255, 255))
        self._spritesList = pygame.sprite.OrderedUpdates()
        self._spritesList.draw(self._scene)
        self._fps = fps
        self._spriteRegistery = spritesRegistery
        self._rootDir = rootDir
        pygame.display.flip()
        self._clock = pygame.time.Clock()
        self._spriteRegs = {}
        self._textRegs = {}

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

        for textReg in self._textRegs.itervalues():
            label = textReg.label
            textPos = label.get_rect()
            textPos.centerx = textReg.x
            textPos.centery = textReg.y
            self._scene.blit(label, textPos)

        pygame.display.flip()

        self._clock.tick(self._fps)

        return True

    def addSprite(self, name, num, x, y):
        try:
            filePath = self._rootDir + '/' + self._spriteRegistery[num]
            sp = SpriteReg(num, filePath, x, y, self._scene)
            self._spritesList.add(sp)
            self._spriteRegs[name] = sp
        except KeyError:
            pass

    def removeSprite(self, name):
        try:
            self._spritesList.remove(self._spriteRegs[name])
        except KeyError:
            pass

    def editSprite(self, name, unevaluatedNum, unevaluatedX, unevaluatedY, evaluation):
        try:
            sp = self._spriteRegs[name]
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
            newFilePath = self._rootDir + '/' + self._spriteRegistery[newNum]
            sp.reload(newNum, newFilePath, newX, newY, self._scene)
        except KeyError:
            pass

    def addText(self, name, text, x, y, color, fontName, fontSize):
        self._textRegs[name] = TextReg(text, x, y, color, fontName, fontSize)

    def removeText(self, name):
        try:
            del self._textRegs[name]
        except KeyError:
            pass

    def editText(self, name, unevaluatedText, unevaluatedX, unevaluatedY, unevaluatedColorName,
                 unevaluatedFontName, unevaluatedFontSize, evaluation):
        label = self._textRegs[name]
        newText = unevaluatedText.value(evaluation, selfParam=label.text)
        if newText == UNDEFINED_PARAMETER:
            newText = label.text
        else:
            newText = str(newText)

        newX = unevaluatedX.value(evaluation, selfParam=label.x)
        if newX == UNDEFINED_PARAMETER:
            newX = label.x
        else:
            newX = int(newX)

        newY = unevaluatedY.value(evaluation, selfParam=label.y)
        if newY == UNDEFINED_PARAMETER:
            newY = label.y
        else:
            newY = int(newY)

        newColorName = unevaluatedColorName.value(evaluation, selfParam=label.colorName)
        if newColorName == UNDEFINED_PARAMETER:
            newColorName = label.colorName
        else:
            newColorName = str(newColorName)

        newFontName = unevaluatedFontName.value(evaluation, selfParam=label.fontName)
        if newFontName == UNDEFINED_PARAMETER:
            newFontName = label.fontName
        else:
            newFontName = str(newFontName)

        newFontSize = unevaluatedFontSize.value(evaluation, selfParam=label.fontSize)
        if newFontSize == UNDEFINED_PARAMETER:
            newFontSize = label.fontSize
        else:
            newFontSize = int(newFontSize)

        label.reload(newText, newX, newY, newColorName, newFontName, newFontSize)

    def hide(self):
        pygame.display.quit()
        self._scene = None