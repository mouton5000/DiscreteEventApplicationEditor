__author__ = 'mouton'

from pygame.mixer import Sound


_rootDir = None


def init(rootDir):
    global _rootDir
    _rootDir = rootDir
    reinit()


def reinit():
    pass


def playSound(filename):
    soundFile = _rootDir + '/' + filename
    sound = Sound(soundFile)
    sound.play()