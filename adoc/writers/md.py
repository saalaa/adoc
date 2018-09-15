"""Markdown writer."""

import io
import logging

from ..errors import FatalError

logger = logging.getLogger(__name__)


def write_md(filename, project, docstring_format='md'):
    with open(filename, 'w') as fh:
        fh.write(
            make_md(project, docstring_format=docstring_format)
        )


def make_md(project, docstring_format='md'):
    if not docstring_format == 'md':
        raise FatalError(
            'unsupported docstring format: {}'.format(docstring_format)
        )

    buf = io.StringIO()

    def write(*text):
        buf.write(
            '{}\n\n'.format(
                ''.join(text).strip()
            )
        )

    def h1(*text):
        write('# ', *text)

    def h2(*text):
        write('## ', *text)

    def h3(*text):
        write('### ', *text)

    def h4(*text):
        write('#### ', *text)

    h1('API Reference')

    for m in project.iter_modules():
        if not m.doc and not m.functions and not m.classes:
            continue

        h2('Module `', m.fully_qualified_name, '`')

        if m.doc:
            write(m.doc)

        for f in m.functions or []:
            h3('Function `', f.name, '(', ', '.join(f.parameters), ')`')

            if f.doc:
                write(f.doc)

        for c in m.classes or []:
            if c.bases:
                h3('Class `', c.name, '(', ', '.join(c.bases), ')`')
            else:
                h3('Class `', c.name, '`')

            if c.doc:
                write(c.doc)

            for f in c.functions or []:
                h4('Method `', f.name, '(', ', '.join(f.parameters), ')`')

                if f.doc:
                    write(f.doc)

    return buf.getvalue()
