from ..errors import FatalError

from .html import write_html
from .md import write_md


def find_writer(args):
    if not args.html and not args.md:
        raise FatalError(
            'no output format specified, use `--html` or `--md`'
        )
    elif args.html:
        return write_html
    elif args.md:
        return write_md
