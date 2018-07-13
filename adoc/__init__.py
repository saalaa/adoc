"""Main package."""

import sys

from .version import version
from .cli import main

__version__ = version


if __name__ == '__main__':

    sys.exit(
        main()
    )
