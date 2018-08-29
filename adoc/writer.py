"""HTML writer."""

import os
import logging
import mako.lookup
import mako.exceptions
import traceback

from .errors import FatalError
from .formats import (
    format_md, format_rst
)

logger = logging.getLogger(__name__)


TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), 'templates'
)


def html(project, docstring_format='md'):
    if docstring_format == 'rst':
        format_doc = format_rst
    else:
        format_doc = format_md

    try:
        lookup = mako.lookup.TemplateLookup(directories=[TEMPLATE_PATH])
        template = lookup.get_template('html.mako')

        return template.render(
            project=project,
            format_md=format_md,
            format_rst=format_rst,
            format_doc=format_doc
        )
    except mako.exceptions.MakoException:
        tb = mako.exceptions.text_error_template() \
            .render()

        raise FatalError(
            'error loading `html.mako`', tb=tb
        )
    except Exception:
        tb = traceback.format_exc()

        # Below, we attempt to provide a nice Mako traceback, which includes
        # relevant Mako templating, but keep a standard formatted traceback in
        # case anything goes wrong.

        try:
            tb = mako.exceptions.text_error_template() \
                .render()
        except Exception:
            pass

        raise FatalError(
            'unknown error while rendering HTML', tb=tb
        )
