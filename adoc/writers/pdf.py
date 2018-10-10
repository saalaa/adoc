import logging

from ..errors import FatalError
from .html import make_html

logger = logging.getLogger(__name__)


class WeasyPrintLogFilter(logging.Filter):
    def filter(self, record):
        if record.levelno >= logging.ERROR:
            logger.error(record.getMessage())
            return False


logging.getLogger('weasyprint') \
    .addFilter(
        WeasyPrintLogFilter()
    )


def write_pdf(filename, project, docstrings_format, strip_docstring):
    with open(filename, 'wb') as fh:
        fh.write(
            make_pdf(project, docstrings_format, strip_docstring)
        )


def make_pdf(project, docstrings_format, strip_docstring):
    try:
        from weasyprint import HTML
    except ImportError:
        raise FatalError(
            'PDF output requires WeasyPrint'
        )

    html = make_html(
        project, docstrings_format, strip_docstring
    )

    html = HTML(string=html)

    return html.write_pdf()
