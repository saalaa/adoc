import os

from functools import wraps


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
        self.target_wd = os.path.abspath(directory)
        self.initial_wd = os.path.abspath(
            os.getcwd()
        )

    def __enter__(self):
        os.chdir(self.target_wd)

    def __exit__(self, *args):
        os.chdir(self.initial_wd)
