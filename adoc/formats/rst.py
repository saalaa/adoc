"""reStructuredText formatter.

This module aims to bring a decent level of compatibility with Sphinx without
relying on anything except `docutils`.

This is obviously still a work in progress.

Docutils resources:

- https://docutils.readthedocs.io/en/sphinx-docs/howto/rst-directives.html
- https://docutils.readthedocs.io/en/sphinx-docs/howto/rst-roles.html

Sphinx resources:

- http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html
- http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
"""

from docutils import core, nodes
from docutils.writers.html4css1 import Writer
from docutils.parsers.rst import (
    directives, roles, Directive
)


class DummyDirective(Directive):
    """Generic directive that does nothing."""
    required_arguments = 1
    optional_arguments = 0

    final_argument_whitespace = True

    has_content = True

    def run(self):
        return []


class VersionAdmonition(Directive):
    """Version-based admonitions.

    Supports the following construction:

        .. deprecated:: 0.1
            This method is ...
    """
    required_arguments = 1
    optional_arguments = 1

    final_argument_whitespace = True

    has_content = True

    version_labels = {
        'deprecated': 'Deprecated since version {}',
        'versionadded': 'New in version {}',
        'versionchanged': 'Changed in version {}'
    }

    def run(self):
        node = nodes.admonition()

        version_label = self.version_labels[self.name]
        label = version_label.format(
            self.arguments[0]
        )

        if len(self.arguments) == 2:
            inodes, messages = self.state.inline_text(
                self.arguments[1], self.lineno + 1
            )

            node.append(
                nodes.paragraph(self.arguments[1], '', *inodes)
            )

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)

        if len(node):
            label = nodes.inline(
                '', '{}: '.format(label), classes=['versionmodified']
            )

            node[0].insert(0, label)
        else:
            label = nodes.inline(
                '', '{}.'.format(label), classes=['versionmodified']
            )

            node.append(
                nodes.paragraph('', '', label)
            )

        return [node]


def dummy_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    return [], []


def symbol_lookup(role, rawtext, text, lineno, inliner, options={},
                  content=[]):
    rawtext.find('`')
    text = rawtext.split('`')[1]
    text = text.lstrip('~')
    node = nodes.literal(rawtext, text)
    return [node], []


def emphasis(role, rawtext, text, lineno, inliner, options={}, content=[]):
    rawtext.find('`')
    text = rawtext.split('`')[1]
    node = nodes.emphasis(rawtext, text)
    return [node], []


def format_rst(text):
    """Format reStructuredText text to HTML."""
    parts = core.publish_parts(
        text, writer=Writer()
    )

    return parts['fragment']


directives.register_directive('autoclass', DummyDirective)
directives.register_directive('describe', DummyDirective)
directives.register_directive('deprecated', VersionAdmonition)
directives.register_directive('versionadded', VersionAdmonition)
directives.register_directive('versionchanged', VersionAdmonition)

roles.register_canonical_role('ref', dummy_role)
roles.register_canonical_role('doc', dummy_role)
roles.register_canonical_role('envvar', symbol_lookup)
roles.register_canonical_role('file', symbol_lookup)
roles.register_canonical_role('mod', symbol_lookup)
roles.register_canonical_role('data', symbol_lookup)
roles.register_canonical_role('func', symbol_lookup)
roles.register_canonical_role('class', symbol_lookup)
roles.register_canonical_role('attr', symbol_lookup)
roles.register_canonical_role('meth', symbol_lookup)
roles.register_canonical_role('exc', symbol_lookup)
roles.register_canonical_role('command', symbol_lookup)
roles.register_canonical_role('mimetype', emphasis)
