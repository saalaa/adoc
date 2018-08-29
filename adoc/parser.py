"""High-level parsing functions."""

import os
import ast
import unittest.mock
import setuptools
import importlib
import fnmatch
import logging

from .utils import WorkingDirectory
from .models import (
    Project, Module, Document
)

# TODO Improve error handling but stick to basic logging here
# TODO Raise exceptions when/where needed

logger = logging.getLogger(__name__)


DEFAULT_EXCLUDE = [
    '*.tests',
    '*.tests.*',
    'tests.*',
    'tests',
    'test_*',
    '*_test.*',
    '*.migrations',
    '*.migrations.*',
    'migrations.*',
    'migrations',
    'migration_*',
    'conftest.*',
]


class ProjectParser:
    module = None

    def __init__(self, path, overrides, no_setup=False, exclude=None,
                 find_packages=False, documents=None):
        self.path = path
        self.overrides = overrides
        self.no_setup = no_setup
        self.find_packages = find_packages
        self.exclude = exclude or DEFAULT_EXCLUDE
        self.documents = documents or []

    def parse(self):
        """Parse a project, setting the current working directiory."""
        logger.debug(
            'entering {}'.format(self.path)
        )

        with WorkingDirectory(self.path):
            return self.parse_project()

    def parse_project(self):
        """Parse a Python project in the current working directory."""
        metadata = {}

        if not self.no_setup and self.setup_exists():
            logger.debug('loading setup.py')

            metadata.update(
                self.load_setup()
            )

        metadata.update(self.overrides)

        if 'package_dir' not in metadata:
            metadata['package_dir'] = {
                '': '.'  # All packages in current directory by default
            }

        if 'name' not in metadata:
            logger.debug('guessing project name')
            metadata['name'] = os.path.basename(
                os.path.realpath(self.path)
            )

        if 'packages' not in metadata or self.find_packages:
            logger.debug('guessing packages')
            metadata['packages'] = setuptools.find_packages(
                metadata['package_dir'].get('', ''), exclude=self.exclude
            )

        readme = self.find_readme()
        if readme:
            logger.debug(
                'found {}'.format(readme)
            )

            readme = Document(readme)

        project = Project(metadata['name'], readme, metadata)

        for document in self.documents:
            logger.debug(
                'adding document {}'.format(document)
            )

            project.add_document(
                Document(document)
            )

        for script in metadata.get('scripts', []):
            logger.debug(
                'parsing script {}'.format(script)
            )

            try:
                module = self.parse_file(script, script, strip_ext=False)
            except SyntaxError:
                logger.error(
                    '{} does not appear to be a Python script'.format(script)
                )

                continue

            if not module.is_empty():
                project.add_module(
                    module
                )

        for package in metadata.get('packages', []):
            logger.debug(
                'parsing package {}'.format(package)
            )

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

    def find_readme(self):
        """Parse a README file in the current working directory."""
        if os.path.isfile('README.md'):
            return 'README.md'

        if os.path.isfile('README.rst'):
            return 'README.rst'

        return None

    def setup_exists(self):
        return os.path.isfile('setup.py')

    def load_setup(self):
        """Parse a `setup.py` file in the current working directory."""
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

    def parse_file(self, path, name, strip_ext=True):
        """Parse a Python file."""
        with open(path) as fh:
            contents = fh.read()

        if strip_ext:
            name, ext = os.path.splitext(name)

        root = ast.parse(contents)

        return Module.from_ast(root, name)
