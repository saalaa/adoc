"""Project modelisation objects.

These data structures allow the modelisation of a project's documentation and
source code.

They are handled mostly while parsing a project's source code and later
transmited to the HTML writer.
"""

import os
import ast

from bs4 import BeautifulSoup

from .formats import format_md, format_rst
from .utils import memoized
from .codegen import (
    make_python, make_signature
)


def walk(root, attr, max_depth=-1):
    yield root

    if max_depth == 0:
        return

    for item in getattr(root, attr) or []:
        yield from walk(item, attr, max_depth - 1)


class Atom:
    """Lowest-level unit representing a source code unit."""
    name = None
    doc = None

    parent = None

    def __init__(self, name, doc=None):
        self.name = name
        self.doc = doc

    def __str__(self):
        return '<{}:{}>'.format(self.type, self.name)

    @property
    def type(self):
        return self.__class__.__name__

    @property
    @memoized
    def fully_qualified_name(self):
        """Recursively generate an `Atom`'s fully qualified name."""
        if not self.parent or isinstance(self.parent, Project):
            return self.name

        return '.'.join([
            self.parent.fully_qualified_name, self.name
        ])

    @classmethod
    def from_ast(cls, node):
        """Build `Atom` instances from an AST node."""
        raise NotImplementedError()  # pragma: no cover


class ParametersMixin:
    """Mixin for classes that hold parameters."""
    parameters = None

    def add_parameters(self, parameters):
        """Add parameters representation (ie. `str`)."""
        if self.parameters is None:
            self.parameters = []

        self.parameters.extend(
            parameters
        )


class DecoratorsMixin:
    """Mixin for classes that hold decorators."""
    decorators = None

    def add_decorators(self, decorators):
        """Add decorators, (ie. `str`)."""
        if self.decorators is None:
            self.decorators = []

        self.decorators.extend(
            decorators
        )


class FunctionsMixin:
    """Mixin for classes that hold `Function` instances."""
    functions = None

    def is_empty(self):
        return not self.functions

    def add_function(self, function):
        """Add a `Function` instance, setting `self` as its parent."""
        if self.functions is None:
            self.functions = []

        function.parent = self

        self.functions.append(function)


class Function(ParametersMixin, DecoratorsMixin, Atom):
    """Representation of a function."""
    @classmethod
    def from_ast(cls, node):
        """Build a `Function` instance from an AST node."""
        doc = ast.get_docstring(node)
        function = cls(node.name, doc)

        function.add_decorators(
            make_python(decorator) for decorator in node.decorator_list
        )

        function.add_parameters(
            make_signature(node.args)
        )

        return function


class ClassesMixin:
    """Mixin for classes that hold `Class` instances."""
    classes = None

    def is_empty(self):
        return not self.classes

    def add_class(self, klass):
        """Add a `Class` instance, setting `self` as its parent."""
        if self.classes is None:
            self.classes = []

        klass.parent = self

        self.classes.append(klass)


class Class(DecoratorsMixin, FunctionsMixin, Atom):
    """Representation of a class."""
    bases = None

    def add_base(self, base):
        if self.bases is None:
            self.bases = []

        self.bases.append(
            base
        )

    @classmethod
    def from_ast(cls, node):
        """Build a `Class` instance from an AST node."""
        doc = ast.get_docstring(node)
        klass = cls(node.name, doc)

        klass.add_decorators(
            make_python(decorator) for decorator in node.decorator_list
        )

        for base in node.bases:
            klass.add_base(
                make_python(base)
            )

        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef):
                klass.add_function(
                    Function.from_ast(child)
                )

        return klass


class ModulesMixin:
    """Mixin for classes that hold `Module` instances."""
    modules = None

    def is_empty(self):
        if not self.modules:
            return True

        for module in self.modules:
            if not module.is_empty():
                return False

        return True

    def add_module(self, module):
        """Add a `Module` instance, setting `self` as its parent."""
        if self.modules is None:
            self.modules = []

        module.parent = self

        self.modules.append(module)


class Module(ModulesMixin, ClassesMixin, FunctionsMixin, Atom):
    """Representation of a module.

    No distinction is made between modules and packages.
    """
    def is_empty(self):
        return FunctionsMixin.is_empty(self) and ClassesMixin.is_empty(self) \
                and ModulesMixin.is_empty(self)

    def merge(self, module):
        self.doc = module.doc  # TODO Merge the rest as well

    @classmethod
    def from_ast(cls, node, name):
        """Build a `Module` instance from an AST node."""
        doc = ast.get_docstring(node)
        module = Module(name, doc)

        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                module.add_class(
                    Class.from_ast(child)
                )

            if isinstance(child, ast.FunctionDef):
                module.add_function(
                    Function.from_ast(child)
                )

        return module


class Project(ModulesMixin, Atom):
    """Representation of a project."""
    name = None
    metadata = None
    documents = None

    def __init__(self, name, doc, metadata=None):
        super().__init__(
            name, doc
        )

        self.metadata = metadata or {}
        self.documents = []

    def add_document(self, document):
        self.documents.append(document)

    def has_meta(self, *keys):
        for key in keys:
            if self.get_meta(key):
                return True

        return False

    def get_meta(self, key, default=None):
        return self.metadata.get(key, default) if self.metadata else default

    def iter_modules(self, max_depth=-1):
        modules = []
        for module in walk(self, 'modules', max_depth=max_depth):
            if getattr(module, 'modules', None):
                modules += module.modules

        return sorted(
            modules, key=lambda m: m.fully_qualified_name
        )

    def iter_functions(self, max_depth=-1):
        functions = []
        for module in walk(self, 'modules', max_depth=max_depth):
            if getattr(module, 'functions', None):
                functions += module.functions

        return sorted(
            functions, key=lambda f: f.name
        )

    def iter_classes(self, max_depth=-1):
        classes = []
        for module in walk(self, 'modules', max_depth=max_depth):
            if getattr(module, 'classes', None):
                classes += module.classes

        return sorted(
            classes, key=lambda c: c.name
        )


class Document:
    """Representation of a document.

    Supported document formats are `html`, `md` and `rst`.
    """
    filename = None
    name = None
    ext = None

    def __init__(self, filename):
        self.filename = os.path.realpath(filename)
        self.name, self.ext = os.path.splitext(
            os.path.basename(self.filename)
        )

    @property
    @memoized
    def html(self):
        """Format a document to HTML.

        The value of this property is cached for better performances.
        """
        def format_html(x):
            return x

        if self.ext not in ('.html', '.md', '.rst'):
            raise Exception(
                'Unsupported document format: {}{}'.format(self.name, self.ext)
            )
        elif self.ext == '.html':
            format_func = format_html
        elif self.ext == '.md':
            format_func = format_md
        elif self.ext == '.rst':
            format_func = format_rst

        with open(self.filename) as fh:
            return format_func(
                fh.read()
            )

    @property
    @memoized
    def title(self):
        """Extract a document's title.

        For this to be possible, it has first to formatted to HTML.

        The value of this property is cached for better performances.
        """
        soup = BeautifulSoup(self.html, 'html.parser')

        headings = soup.find_all('h1')
        if len(headings):
            return ' '.join(headings[0].contents)

        return self.name
