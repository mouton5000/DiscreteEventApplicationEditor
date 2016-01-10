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

    def export(self):
        return 'KEYWORD_X'

KEYWORD_X = _KeyWordX()


class _KeyWordY(_Keyword):
    def __str__(self):
        return 'kw_y'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_Y'

KEYWORD_Y = _KeyWordY()


class _KeyWordZ(_Keyword):
    def __str__(self):
        return 'kw_z'

    def __repr__(self):
        return str(self)


    def export(self):
        return 'KEYWORD_Z'

KEYWORD_Z = _KeyWordZ()


class _KeyWordXInt(object):

    class keydefaultdict(defaultdict):
        def __missing__(self, key):
            ret = self[key] = self.default_factory(key)
            return ret

    class _NewKeyword(_Keyword):

        def __init__(self, index):
            super(_KeyWordXInt._NewKeyword, self).__init__()
            self._index = index

        def __str__(self):
            return 'kw_x(' + str(id(self)) + ')'

        def export(self):
            return 'KEYWORD_X_INT[' + str(self._index) + ']'

    keywords = keydefaultdict(_NewKeyword)

    def __getitem__(self, index):
        return _KeyWordXInt.keywords[index]

    def export(self):
        return 'KEYWORD_X_INT'

KEYWORD_X_INT = _KeyWordXInt()


class _KeyWordYInt(object):
    class keydefaultdict(defaultdict):
        def __missing__(self, key):
            ret = self[key] = self.default_factory(key)
            return ret

    class _NewKeyword(_Keyword):

        def __init__(self, index):
            super(_KeyWordYInt._NewKeyword, self).__init__()
            self._index = index

        def __str__(self):
            return 'kw_y(' + str(id(self)) + ')'

        def export(self):
            return 'KEYWORD_Y_INT[' + str(self._index) + ']'

    def __repr__(self):
        return str(self)

    keywords = keydefaultdict(_NewKeyword)

    def __getitem__(self, index):
        return _KeyWordYInt.keywords[index]

KEYWORD_Y_INT = _KeyWordYInt()


class _KeyWordW(_Keyword):
    def __str__(self):
        return 'kw_w'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_W'


KEYWORD_W = _KeyWordW()


class _KeyWordH(_Keyword):
    def __str__(self):
        return 'kw_h'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_H'

KEYWORD_H = _KeyWordH()


class _KeyWordRotate(_Keyword):
    def __str__(self):
        return 'kw_rotate'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_ROTATE'

KEYWORD_ROTATE = _KeyWordRotate()


class _KeyWordScale(_Keyword):
    def __str__(self):
        return 'kw_scale'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_SCALE'

KEYWORD_SCALE = _KeyWordScale()


class _KeyWordFileName(_Keyword):
    def __str__(self):
        return 'kw_fileName'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_FILENAME'

KEYWORD_FILENAME = _KeyWordFileName()


class _KeyWordWidth(_Keyword):
    def __str__(self):
        return 'kw_width'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_WIDTH'

KEYWORD_WIDTH = _KeyWordWidth()


class _KeyWordColor(_Keyword):
    def __str__(self):
        return 'kw_color'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_COLOR'

KEYWORD_COLOR = _KeyWordColor()


class _KeyWordText(_Keyword):
    def __str__(self):
        return 'kw_text'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_TEXT'

KEYWORD_TEXT = _KeyWordText()


class _KeyWordFontName(_Keyword):
    def __str__(self):
        return 'kw_fontName'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_FONT_NAME'

KEYWORD_FONT_NAME = _KeyWordFontName()


class _KeyWordFontSize(_Keyword):
    def __str__(self):
        return 'kw_fontSize'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_FONT_SIZE'

KEYWORD_FONT_SIZE = _KeyWordFontSize()


class _KeyWordId(_Keyword):
    def __str__(self):
        return 'kw_id'

    def __repr__(self):
        return str(self)

    def export(self):
        return 'KEYWORD_ID'

KEYWORD_ID = _KeyWordId()