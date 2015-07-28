from collections import defaultdict

__author__ = 'mouton'


class _Keyword(object):
    def __init__(self):
        pass

    def value(self, _):
        return self


class _KeyWordX(_Keyword):
    def __str__(self):
        return 'kw_x'

    def __repr__(self):
        return str(self)

KEYWORD_X = _KeyWordX()


class _KeyWordY(_Keyword):
    def __str__(self):
        return 'kw_y'

    def __repr__(self):
        return str(self)

KEYWORD_Y = _KeyWordY()


class _KeyWordXInt(object):
    class _NewKeyword(_Keyword):
        def __str__(self):
            return 'kw_x(' + str(id(self)) + ')'

    def __repr__(self):
        return str(self)

    keywords = defaultdict(lambda: _KeyWordXInt._NewKeyword())

    def __getitem__(self, index):
        return _KeyWordXInt.keywords[index]


KEYWORD_X_INT = _KeyWordXInt()


class _KeyWordYInt(object):
    class _NewKeyword(_Keyword):
        def __str__(self):
            return 'kw_y(' + str(id(self)) + ')'

    def __repr__(self):
        return str(self)

    @staticmethod
    def _getNewKeyWordYInt():
        return _KeyWordYInt._NewKeyword()

    keywords = defaultdict(lambda: _KeyWordYInt._NewKeyword())

    def __getitem__(self, index):
        return _KeyWordYInt.keywords[index]


KEYWORD_Y_INT = _KeyWordYInt()


class _KeyWordW(_Keyword):
    def __str__(self):
        return 'kw_w'

    def __repr__(self):
        return str(self)

KEYWORD_W = _KeyWordW()


class _KeyWordH(_Keyword):
    def __str__(self):
        return 'kw_h'

    def __repr__(self):
        return str(self)

KEYWORD_H = _KeyWordH()


class _KeyWordRotate(_Keyword):
    def __str__(self):
        return 'kw_rotate'

    def __repr__(self):
        return str(self)

KEYWORD_ROTATE = _KeyWordRotate()


class _KeyWordScale(_Keyword):
    def __str__(self):
        return 'kw_scale'

    def __repr__(self):
        return str(self)

KEYWORD_SCALE = _KeyWordScale()


class _KeyWordCode(_Keyword):
    def __str__(self):
        return 'kw_code'

    def __repr__(self):
        return str(self)

KEYWORD_CODE = _KeyWordCode()


class _KeyWordWidth(_Keyword):
    def __str__(self):
        return 'kw_width'

    def __repr__(self):
        return str(self)

KEYWORD_WIDTH = _KeyWordWidth()


class _KeyWordColor(_Keyword):
    def __str__(self):
        return 'kw_color'

    def __repr__(self):
        return str(self)

KEYWORD_COLOR = _KeyWordColor()


class _KeyWordText(_Keyword):
    def __str__(self):
        return 'kw_text'

    def __repr__(self):
        return str(self)

KEYWORD_TEXT = _KeyWordText()


class _KeyWordFontName(_Keyword):
    def __str__(self):
        return 'kw_fontName'

    def __repr__(self):
        return str(self)

KEYWORD_FONT_NAME = _KeyWordFontName()


class _KeyWordFontSize(_Keyword):
    def __str__(self):
        return 'kw_fontSize'

    def __repr__(self):
        return str(self)

KEYWORD_FONT_SIZE = _KeyWordFontSize()


class _KeyWordId(_Keyword):
    def __str__(self):
        return 'kw_id'

    def __repr__(self):
        return str(self)

KEYWORD_ID = _KeyWordId()