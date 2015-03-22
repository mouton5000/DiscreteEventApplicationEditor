__author__ = 'mouton'


def sign(x):
    if isinstance(x, str):
        raise TypeError

    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1