from ..errors import FatalError

from .html import write_html
from .md import write_md
from .pdf import write_pdf


def find_writer(args):
    if not args.html and not args.md and not args.pdf:
        raise FatalError(
            'no output format specified, use `--html`, `--md` or `--pdf`'
        )
    elif args.html:
        return write_html
    elif args.md:
        return write_md
    elif args.pdf:
        return write_pdf
