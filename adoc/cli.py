"""Command-line interface.

This module exports the program's entry point: `main`.
"""

import argparse
import sys
import traceback

from .version import version
from .writer import html
from .utils import error, success
from .parser import ProjectParser
from .httpd import Server


def main():
    """Program entry point.

    This is where command line arguments are configured and read. Then the
    configuration is fine-tuned for execution.
    """
    ap = argparse.ArgumentParser(prog='adoc', description='A Python '
                                 'documentation generation tool')

    ap.add_argument('--version', action='version',
                    version='%(prog)s ' + version)

    ap.add_argument('-v', action='store_true',
                    help='run in verbose mode')

    ap.add_argument('-o', '--output', type=str,
                    help='output file')

    ap.add_argument('-d', action='append', metavar='DOCUMENT',
                    help='additional document')

    ap.add_argument('--rst-docstrings', action='store_true',
                    help='format docstrings using RST')

    ap.add_argument('--no-setup', action='store_true',
                    help='disable parsing of `setup.py`')

    ap.add_argument('--project-name', type=str,
                    help='override project name')

    ap.add_argument('--project-version', type=str,
                    help='override project version')

    ap.add_argument('--package-dir', type=str,
                    help='override package directory')

    ap.add_argument('--packages', type=str,
                    help='override packages')

    ap.add_argument('--find-packages', action='store_true',
                    help='force-find packages using setuptools')

    ap.add_argument('--exclude', type=str, action='append',
                    help='set excluded packages')

    ap.add_argument('--serve', action='store_true',
                    help='serve documentation over HTTP')

    ap.add_argument('--host', type=str, default='0.0.0.0',
                    help='live-server host, defaults to 0.0.0.0')

    ap.add_argument('--port', type=int, default='8080',
                    help='live-server port, defaults to 8080')

    ap.add_argument('project_path', metavar='PROJECT_PATH',
                    help='project path')

    args = ap.parse_args(sys.argv[1:])

    docstrings_format = 'rst' if args.rst_docstrings else 'md'

    metadata = {}

    if args.project_name:
        metadata['name'] = args.project_name

    if args.project_version:
        metadata['version'] = args.project_version

    if args.package_dir:
        metadata['package_dir'] = {
            '': args.package_dir
        }

    exclude = None
    if args.exclude:
        exclude = args.exclude.split(',')

    parser = ProjectParser(args.project_path, metadata, no_setup=args.no_setup,
                           force_find_packages=args.find_packages,
                           exclude=exclude, documents=args.d)

    if args.serve:
        server = Server(args.host, args.port, parser, docstrings_format)

        success('Server live at http://%s:%s' % (args.host, args.port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            return 0
        except Exception:
            if not args.verbose:
                error('An exception occured, use `-v` if you want a traceback')
            else:
                error('An exception occured, traceback follows')
                traceback.print_exc(file=sys.stderr)

            return 1
    else:
        project = parser.parse()

        output = sys.stdout
        if args.output:
            output = open(args.output, 'w')

        output.write(
            html(project, docstrings_format)
        )

        return 0
