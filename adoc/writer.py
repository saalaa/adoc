# import re
import os
import markdown

from mako.lookup import TemplateLookup

template_path = os.path.join(
    os.path.dirname(__file__), 'templates'
)

template_lookup = TemplateLookup(directories=[template_path], cache_args={
    'cached': True,
    'cache_type': 'memory'
})


def doc_filter(converter, resolver, atom):
    def replacer(match):
        match = match.group(0)

        link, name = resolver(match)

        if link is None:
            return match

        return '[`%s`](%s)' % (name, link)

    # print(
    #     atom
    # )

    # doc, _ = re.subn('`[^`]+`', replacer, atom.doc)

    doc = atom

    return converter(doc)


def make_ancestor_filter(resolver):
    def ancestor_filter(text):
        link, name = resolver(text)
        return link

    return ancestor_filter


def make_resolver(project, stdlib_fallback=False):
    def resolver(name):
        atom = project.resolve(name)

        if atom:
            return '#' + atom.fully_qualified_name, atom.name

        if stdlib_fallback:
            return 'https://docs.python.org/3/search.html?q=%s' + name, name

        return None, None

    return resolver


def format_doc(atom):
    doc = atom.doc

    return markdown.markdown(doc, extentions=[
        'markdown.extensions.codehilite'
    ])


# def resolve(context, name, context):


def html(project):
    return template_lookup.get_template('html.mako') \
            .render(project=project, format_doc=format_doc)
