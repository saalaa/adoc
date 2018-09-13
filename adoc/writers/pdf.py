import logging

from weasyprint import HTML

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


def write_pdf(filename, project, docstring_format='md'):
    with open(filename, 'wb') as fh:
        fh.write(
            make_pdf(project, docstring_format=docstring_format)
        )


def make_pdf(project, docstring_format='md'):

    html = make_html(
        project, docstring_format=docstring_format
    )

    html = HTML(string=html)

    return html.write_pdf()
