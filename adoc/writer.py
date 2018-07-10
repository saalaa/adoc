import os
import markdown
import mako.lookup

from docutils import core
from docutils.writers.html4css1 import Writer


TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), 'templates'
)


def format_md(text):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite'
    ])

    return md.convert(text)


def format_rst(text):
    parts = core.publish_parts(
        text, writer=Writer()
    )

    return parts['fragment']


def html(project, docstring_format='md'):
    template_lookup = mako.lookup.TemplateLookup(directories=[TEMPLATE_PATH])
    template = template_lookup.get_template('html.mako')

    if docstring_format == 'rst':
        format_doc = format_rst
    else:
        format_doc = format_md

    return template.render(project=project, format_md=format_md,
            format_rst=format_rst, format_doc=format_doc)
