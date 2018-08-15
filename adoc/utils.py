import os
import sys
import crayons

from functools import wraps


def success(message):
    sys.stdout.write(
        message
    )


def warning(message):
    label = crayons.yellow('Warning')
    sys.stdout.write(
        '{}: {}\n'.format(label, message)
    )


def error(message):
    label = crayons.red('Error')
    sys.stderr.write(
        '{}: {}\n'.format(label, message)
    )

    return 1


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


class WorkingDirectory:
    def __init__(self, directory):
        self.target_wd = directory
        self.initial_wd = os.getcwd()

    def __enter__(self):
        os.chdir(self.target_wd)

    def __exit__(self, *args):
        os.chdir(self.initial_wd)
