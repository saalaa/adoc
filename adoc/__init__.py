"""Main package."""

import sys

from .version import version

__version__ = version


if __name__ == '__main__':
    from .cli import main

    sys.exit(
        main()
    )
