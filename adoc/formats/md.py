"""Markdown formatter."""

import markdown

md_converter = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite'
])


def format_md(text):
    return md_converter.convert(text)
