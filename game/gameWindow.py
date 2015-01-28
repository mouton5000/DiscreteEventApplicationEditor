from pygame.rect import Rect
from game.Registeries import SpriteReg, TextReg, LineReg, RectReg

__author__ = 'mouton'

import pygame
from pygame import Color
from database import Event, UNDEFINED_PARAMETER


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
        self._lineRegs = {}
        self._rectRegs = {}

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Event.events.add(Event('Mouse', [event.pos[0], event.pos[1]]))
        self._scene.fill((255, 255, 255))

        for lineReg in self._lineRegs.itervalues():
            color = Color('#' + lineReg.colorName)
            pygame.draw.line(self._scene, color, (lineReg.x1, lineReg.y1), (lineReg.x2, lineReg.y2), lineReg.width)

        for rectReg in self._rectRegs.itervalues():
            color = Color('#' + rectReg.colorName)
            pygame.draw.rect(self._scene, color, Rect(rectReg.x, rectReg.y, rectReg.w, rectReg.h), rectReg.width)

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

    def addLine(self, name, x1, y1, x2, y2, width, colorName):
        self._lineRegs[name] = LineReg(x1, y1, x2, y2, width, colorName)

    def removeLine(self, name):
        try:
            del self._lineRegs[name]
        except KeyError:
            pass

    def editLine(self, name, unevaluatedX1, unevaluatedY1, unevaluatedX2, unevaluatedY2,
                 unevaluatedWidth, unevaluatedColorName, evaluation):
        try:
            line = self._lineRegs[name]
        except KeyError:
            return

        newX1 = unevaluatedX1.value(evaluation, selfParam=line.x1)
        if newX1 == UNDEFINED_PARAMETER:
            newX1 = line.x1
        else:
            newX1 = int(newX1)

        newY1 = unevaluatedY1.value(evaluation, selfParam=line.y1)
        if newY1 == UNDEFINED_PARAMETER:
            newY1 = line.y1
        else:
            newY1 = int(newY1)

        newX2 = unevaluatedX2.value(evaluation, selfParam=line.x2)
        if newX2 == UNDEFINED_PARAMETER:
            newX2 = line.x2
        else:
            newX2 = int(newX2)

        newY2 = unevaluatedY2.value(evaluation, selfParam=line.y2)
        if newY2 == UNDEFINED_PARAMETER:
            newY2 = line.y2
        else:
            newY2 = int(newY2)

        newWidth = unevaluatedWidth.value(evaluation, selfParam=line.width)
        if newWidth == UNDEFINED_PARAMETER:
            newWidth = line.width
        else:
            newWidth = int(newWidth)

        newColorName = unevaluatedColorName.value(evaluation, selfParam=line.colorName)
        if newColorName == UNDEFINED_PARAMETER:
            newColorName = line.colorName
        else:
            newColorName = str(newColorName)

        line.reload(newX1, newY1, newX2, newY2, newWidth, newColorName)

    def addRect(self, name, x, y, w, h, width, colorName):
        self._rectRegs[name] = RectReg(x, y, w, h, width, colorName)

    def removeRect(self, name):
        try:
            del self._rectRegs[name]
        except KeyError:
            pass

    def editRect(self, name, unevaluatedX, unevaluatedY, unevaluatedW, unevaluatedH,
                 unevaluatedWidth, unevaluatedColorName, evaluation):
        try:
            rect = self._rectRegs[name]
        except KeyError:
            return

        newX = unevaluatedX.value(evaluation, selfParam=rect.x)
        if newX == UNDEFINED_PARAMETER:
            newX = rect.x
        else:
            newX = int(newX)

        newY = unevaluatedY.value(evaluation, selfParam=rect.y)
        if newY == UNDEFINED_PARAMETER:
            newY = rect.y
        else:
            newY = int(newY)

        newW = unevaluatedW.value(evaluation, selfParam=rect.w)
        if newW == UNDEFINED_PARAMETER:
            newW = rect.w
        else:
            newW = int(newW)

        newH = unevaluatedH.value(evaluation, selfParam=rect.h)
        if newH == UNDEFINED_PARAMETER:
            newH = rect.h
        else:
            newH = int(newH)

        newWidth = unevaluatedWidth.value(evaluation, selfParam=rect.width)
        if newWidth == UNDEFINED_PARAMETER:
            newWidth = rect.width
        else:
            newWidth = int(newWidth)

        newColorName = unevaluatedColorName.value(evaluation, selfParam=rect.colorName)
        if newColorName == UNDEFINED_PARAMETER:
            newColorName = rect.colorName
        else:
            newColorName = str(newColorName)

        rect.reload(newX, newY, newW, newH, newWidth, newColorName)

    def hide(self):
        pygame.display.quit()
        self._scene = None