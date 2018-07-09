"""High-level parsing functions."""

import os
import ast

from .utils import warning
from .ignores import matches
from .models import (
    Project, Module
)


def parse(path, ignores):
    """Main parsing function"""
    return parse_project(path, ignores)


def parse_project(path, ignores):
    """Parse a Python project."""
    name = os.path.basename(
        os.path.realpath(path)
    )

    readme = os.path.join(path, 'README.md')

    doc = None
    if os.path.isfile(readme):
        with open(readme) as file:
            doc = file.read()
    else:
        warning('README.md not found in project')

    project = Project(name, doc)

    for item in os.listdir(path):
        fullpath = os.path.join(path, item)

        if matches(fullpath, item, ignores):
            continue

        if not os.path.isdir(fullpath):
            continue

        module = parse_module(path, item, ignores)

        if not module.is_empty():
            project.add_module(module)

    return project


def parse_module(path, name, ignores):
    """Parse a Python module."""
    module_path = os.path.join(path, name)

    current_module = Module(name)

    init = os.path.join(module_path, '__init__.py')
    if os.path.isfile(init):
        current_module.merge(
            parse_file(module_path, '__init__.py')
        )

    for item in os.listdir(module_path):
        item_path = os.path.join(module_path, item)

        if matches(item_path, item, ignores):
            continue

        if os.path.isdir(item_path):
            module = parse_module(module_path, item, ignores)

            if not module.is_empty():
                current_module.add_module(module)

        if os.path.isfile(item_path):
            if not item_path.endswith('.py'):
                continue

            if item_path.endswith('__init__.py'):
                continue
            if item_path.endswith('__main__.py'):
                continue

            module = parse_file(module_path, item)

            if not module.is_empty():
                current_module.add_module(module)

    return current_module


def parse_file(path, name):
    """Parse a Python file."""
    fullpath = os.path.join(path, name)
    with open(fullpath) as file:
        contents = file.read()

    name, ext = os.path.splitext(name)

    root = ast.parse(contents)

    return Module.from_ast(root, name)
