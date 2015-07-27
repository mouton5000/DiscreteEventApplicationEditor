from collections import defaultdict

__author__ = 'mouton'


class _Keyword(object):
    def __init__(self):
        pass

    def value(self, _):
        return self


class _KeyWordX(_Keyword):
    pass

KEYWORD_X = _KeyWordX()


class _KeyWordY(_Keyword):
    pass

KEYWORD_Y = _KeyWordY()


class _KeyWordXInt(object):
    class _NewKeyword(_Keyword):
        pass

    keywords = defaultdict(lambda: _KeyWordXInt._NewKeyword())

    def __getitem__(self, index):
        return _KeyWordXInt.keywords[index]


KEYWORD_X_INT = _KeyWordXInt()


class _KeyWordYInt(object):
    class _NewKeyword(_Keyword):
        pass

    @staticmethod
    def _getNewKeyWordYInt():
        return _KeyWordYInt._NewKeyword()

    keywords = defaultdict(lambda: _KeyWordYInt._NewKeyword())

    def __getitem__(self, index):
        return _KeyWordYInt.keywords[index]


KEYWORD_Y_INT = _KeyWordYInt()


class _KeyWordW(_Keyword):
    pass

KEYWORD_W = _KeyWordW()


class _KeyWordH(_Keyword):
    pass

KEYWORD_H = _KeyWordH()


class _KeyWordCode(_Keyword):
    pass

KEYWORD_CODE = _KeyWordCode()


class _KeyWordWidth(_Keyword):
    pass

KEYWORD_WIDTH = _KeyWordWidth()


class _KeyWordColor(_Keyword):
    pass

KEYWORD_COLOR = _KeyWordColor()


class _KeyWordText(_Keyword):
    pass

KEYWORD_TEXT = _KeyWordText()


class _KeyWordFontName(_Keyword):
    pass

KEYWORD_FONT_NAME = _KeyWordFontName()


class _KeyWordFontSize(_Keyword):
    pass

KEYWORD_FONT_SIZE = _KeyWordFontSize()


class _KeyWordId(_Keyword):
    pass

KEYWORD_ID = _KeyWordId()