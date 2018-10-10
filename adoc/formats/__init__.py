import re

from .md import format_md
from .rst import format_rst

__all__ = [
    'as_is',
    'stripper',
    'format_md',
    'format_rst'
]

DOCUMENT_MARKER = re.compile(r'^---$', re.M)


def as_is(text):
    return text


def stripper(text):
    match = DOCUMENT_MARKER.search(text)

    if not match:
        return text

    i = match.start()
    return text[:i]
