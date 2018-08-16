"""Markdown formatter."""

import markdown

md_converter = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite'
])


def format_md(text):
    """Format Markdown text to HTML."""
    return md_converter.convert(text)
