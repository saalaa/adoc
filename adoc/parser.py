"""Project and Python parsing functions.

"""
import os
import ast

from .utils import warning
from .models import (
    Project, Module
)


def parse(path):
    return parse_project(path)


def parse_project(path):
    name = os.path.basename(path)
    readme = os.path.join(path, 'README.md')

    doc = None
    if os.path.isfile(readme):
        with open(readme) as file:
            doc = file.read()
    else:
        warning('README.md not found in project')

    project = Project(name, doc)

    # sources = os.path.join(path, name)

    # for module in parse_module(path, name):
    #     project.modules.append(module)

    project.add_module(
        parse_module(path, name)
    )

    # fullpath = os.path.join(path, 'docs')
    # if os.path.isdir(fullpath):
    #     for item in os.walk(fullpath):
    #         print(item)

    return project


def parse_module(path, name):
    fullpath = os.path.join(path, name)

    if os.path.isfile(fullpath):
        return parse_file(path, name)
    elif os.path.isdir(fullpath):
        module = Module(name)

        init = os.path.join(fullpath, '__init__.py')
        if os.path.isfile(init):
            module.merge(
                parse_file(fullpath, '__init__.py')
            )

        path = os.path.join(path, name)
        for item in os.listdir(path):
            fullpath = os.path.join(path, item)

            if fullpath.endswith('__init__.py'):
                continue
            if fullpath.endswith('__main__.py'):
                continue
            if fullpath.endswith('__pycache__'):
                continue

            if os.path.isdir(fullpath):
                module.add_module(
                    parse_module(path, item)
                )
            elif os.path.isfile(fullpath):
                if not fullpath.endswith('.py'):
                    continue

                module.add_module(
                    parse_module(path, item)
                )

        return module


def parse_file(path, name):
    fullpath = os.path.join(path, name)
    with open(fullpath) as file:
        contents = file.read()

    name, ext = os.path.splitext(name)

    root = ast.parse(contents)

    return Module.from_ast(root, name)
