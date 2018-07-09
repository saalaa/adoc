import sys

from functools import wraps


def success(message):
    print(
        message, file=sys.stdout
    )


def warning(message):
    print(
        'Warning: {}'.format(message), file=sys.stderr
    )


def error(message):
    print(
        'Error: {}'.format(message), file=sys.stderr
    )


def memoized(f):
    f._cache = {}

    @wraps(f)
    def wrapper(*args, **kwargs):
        if args in f._cache:
            return f._cache[args]

        value = f(*args, **kwargs)

        f._cache[args] = value

        return value

    return wrapper
