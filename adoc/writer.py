"""HTML writer."""

import os
import mako.lookup
import mako.exceptions

from .formats import (
    format_md, format_rst
)

# TODO Stop leaking Mako exceptions: raise, catch and log our owns
# TODO Provide detailed error information when run in --verbose mode


TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), 'templates'
)


def html(project, docstring_format='md'):
    template_lookup = mako.lookup.TemplateLookup(directories=[TEMPLATE_PATH])
    template = template_lookup.get_template('html.mako')

    if docstring_format == 'rst':
        format_doc = format_rst
    else:
        format_doc = format_md

    # try:
    return template.render(
        project=project,
        format_md=format_md,
        format_rst=format_rst,
        format_doc=format_doc
    )
    # except:
    #     mako.exceptions.text_error_template().render()
