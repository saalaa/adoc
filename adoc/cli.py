"""Command-line interface.

This module exports the program's entry point: `main`.
"""

import argparse
import sys
import traceback

from .writer import html
from .utils import error, success
from .parser import ProjectParser
from .httpd import Server


def main():
    """Program entry point.

    This is where command line arguments are configured and read. Then the
    configuration is fine-tuned for execution.
    """
    argparser = argparse.ArgumentParser(prog='adoc', description='A Python '
            'documentation generation tool')

    argparser.add_argument('-v', action='store_true', help='run in verbose '
            'mode')

    argparser.add_argument('--rst-docstrings', action='store_true',
            help='format docstrings using RST')

    argparser.add_argument('--no-setup', action='store_true', help='disable '
            'parsing of `setup.py`')

    argparser.add_argument('--name', type=str, help='override project name')
    argparser.add_argument('--version', type=str, help='override project '
            'version')
    argparser.add_argument('--package-dir', type=str, help='override package '
            'directory')
    argparser.add_argument('--packages', type=str, help='override packages')

    argparser.add_argument('--find-packages', action='store_true',
            help='force-find packages using setuptools')
    argparser.add_argument('--exclude', type=str, action='append',
            help='set excluded packages')

    argparser.add_argument('--serve', action='store_true',
            help='serve documentation over HTTP')

    argparser.add_argument('--host', type=str, default='0.0.0.0',
            help='live-server host, defaults to 0.0.0.0')

    argparser.add_argument('--port', type=int, default='8080',
            help='live-server port, defaults to 8080')

    argparser.add_argument('project_path', metavar='PROJECT_PATH',
            help='project path')

    args = argparser.parse_args(sys.argv[1:])

    docstrings_format = 'rst' if args.rst_docstrings else 'md'

    metadata = {}

    if args.name:
        metadata['name'] = args.name

    if args.version:
        metadata['version'] = args.version

    if args.package_dir:
        metadata['package_dir'] = {
            '': args.package_dir
        }

    exclude = args.exclude.split(',') if args.exclude else ['*.tests',
            '*.tests.*', 'tests.*', 'tests', 'test_*']

    parser = ProjectParser(args.project_path, metadata, no_setup=args.no_setup,
            force_find_packages=args.find_packages, exclude=exclude)

    if args.serve:
        server = Server(args.host, args.port, parser, docstrings_format)

        success('Starting up on %s:%s' % (args.host, args.port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            return 0
        except:
            if not args.verbose:
                error('An exception occured, use `-v` if you want a traceback')
            else:
                error('An exception occured, traceback follows')
                traceback.print_exc(file=sys.stderr)

            return 1
    else:
        project = parser.parse()

        sys.stdout.write(
            html(project, docstrings_format)
        )

        return 0
