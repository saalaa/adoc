import os

from fnmatch import fnmatchcase

DEFAULTS = [
    'env',
    'docs',
    'tests',
    'migrations',
    '__pycache__',
    'test_*',
    '.env',
    '.git',
    '.hg'
]


def merge_ignores(*ignores):
    uniques = set()
    for items in ignores:
        uniques.update(items or [])

    uniques.update(DEFAULTS)

    return list(uniques)


def find_ignore(path):
    """Find an ignore file through a series of heuristics.

    The following common ignore files are probed:

    - `.gitignore`
    - `.hgignore`
    - `.agignore`
    - `.ignore`
    """
    paths = [
        os.path.join(path, '.gitignore'),
        os.path.join(path, '.hgignore'),
        os.path.join(path, '.agignore'),
        os.path.join(path, '.ignore'),
    ]

    for path in paths:
        if os.path.exists(path) and os.path.isfile(path):
            return path


def read_ignore(filename):
    if not filename:
        return

    ignores = []
    with open(filename) as fh:
        for line in fh.readlines():
            line = line.strip()
            line = line.rstrip('/')

            if not line or line.startswith('#'):
                continue

            ignores.append(line)

    return ignores


def matches(filepath, basename, ignores):
    for pattern in ignores:
        if fnmatchcase(filepath, pattern):
            return True

        if fnmatchcase(basename, pattern):
            return True

    return False
