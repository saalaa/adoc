"""High-level parsing functions."""

import os
import json
import ast
import sys
import unittest.mock
import setuptools
import importlib
import fnmatch

from .utils import warning, WorkingDirectory
from .models import (
    Project, Module
)


class ProjectParser:
    module = None

    def __init__(self, path, overrides, no_setup=False,
            force_find_packages=False, exclude=None):
        self.path = path
        self.overrides = overrides
        self.no_setup = no_setup
        self.force_find_packages = force_find_packages
        self.exclude = exclude or []

    def parse(self):
        """Parse a project, setting the current working directiory."""
        with WorkingDirectory(self.path):
            return self.parse_project()

    def parse_project(self):
        """Parse a Python project in the current working directory."""
        readme = self.parse_readme()

        metadata = {}

        if not self.no_setup:
            metadata.update(
                self.parse_setup()
            )

        metadata.update(self.overrides)

        if 'name' not in metadata:
            metadata['name'] = os.path.basename(
                os.path.realpath(self.path)
            )

        if 'package_dir' not in metadata:
            metadata['package_dir'] = {
                '': '.'  # By default, all packages are in the current directory
            }

        if 'packages' not in metadata or self.force_find_packages:
            metadata['packages'] = setuptools.find_packages(
                metadata['package_dir'].get('', ''), exclude=self.exclude
            )

        project = Project(metadata['name'], readme, metadata)

        for package in metadata['packages']:
            parts = package.split('.')
            dir = metadata['package_dir'].get(
                package, metadata['package_dir'].get('')
            )

            package_path = os.path.join(dir, *parts)

            if not os.path.isdir(package_path):
                continue

            module = self.parse_module(package_path, package)

            if not module.is_empty():
                project.add_module(module)

        return project

    def parse_readme(self):
        """Parse a `README.md` file in the current working directory."""
        if not os.path.isfile('README.md'):
            return None

        with open('README.md') as fh:
            return fh.read()

    def parse_setup(self):
        """Parse a `setup.py` file in the current working directory."""
        if not os.path.isfile('setup.py'):
            return {}

        with unittest.mock.patch.object(setuptools, 'setup') as mock_setup:
            spec = importlib.util.spec_from_file_location('setup', 'setup.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        args, kwargs = mock_setup.call_args

        return kwargs

    def parse_module(self, path, name):
        """Parse a Python module."""
        current_module = Module(name)

        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            if not os.path.isfile(item_path):
                continue

            if not item_path.endswith('.py'):
                continue

            if item_path.endswith('__init__.py'):
                continue

            if item_path.endswith('__main__.py'):
                continue

            excluded = any(
                fnmatch.fnmatchcase(item, pat=excl) for excl in self.exclude
            )

            if excluded:
                continue

            module = self.parse_file(item_path, item)

            if item == '__init__.py':
                current_module.merge(module)
            elif not module.is_empty():
                current_module.add_module(module)

        return current_module

    def parse_file(self, path, name):
        """Parse a Python file."""
        with open(path) as fh:
            contents = fh.read()

        name, ext = os.path.splitext(name)

        root = ast.parse(contents)

        return Module.from_ast(root, name)
