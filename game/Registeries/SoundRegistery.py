__author__ = 'mouton'

from pygame.mixer import Sound


_soundsDictionnary = None
_rootDir = None


def init(soundsDictionnary, rootDir):
    global _soundsDictionnary, _rootDir
    _soundsDictionnary = soundsDictionnary
    _rootDir = rootDir
    reinit()


def reinit():
    pass


def playSound(num):
    soundFile = _rootDir + '/' + _soundsDictionnary[num]
    sound = Sound(soundFile)
    sound.play()