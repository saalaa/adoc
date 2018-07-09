import os
import markdown
import mako.lookup

template_path = os.path.join(
    os.path.dirname(__file__), 'templates'
)

template_lookup = mako.lookup.TemplateLookup(directories=[template_path])


def format_doc(atom):
    return markdown.markdown(atom.doc, extentions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite'
    ])


def html(project):
    return template_lookup.get_template('html.mako') \
            .render(project=project, format_doc=format_doc)
