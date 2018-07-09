"""Command-line interface.

This module provides CLI-related functionalities such as the various commands,
arguments/options parsing and live CLI documentation.

Since *docstrings* in this module are also used by `click` to provide live
CLI documentation, they might sound slightly out of tone.

This module also exports the program's entrypoint: `main`.
"""

import argparse
import sys
import traceback

from .parser import parse
from .writer import html
from .utils import error, success
from .httpd import Server
from .ignores import (
    merge_ignores, find_ignore, read_ignore
)


def main():
    argparser = argparse.ArgumentParser(prog='adoc', description='A Python '
            'documentation generation tool')
    argparser.add_argument('-v', action='store_true',
            help='run in verbose mode')
    argparser.add_argument('-i', '--ignore', type=str, action='append',
            help='define ignored paths')
    argparser.add_argument('--serve', action='store_true',
            help='serve documentation over HTTP')
    argparser.add_argument('--host', type=str, default='0.0.0.0',
            help='HTTP server host, defaults to 0.0.0.0')
    argparser.add_argument('--port', type=int, default='8080',
            help='HTTP server port, defaults to 8080')
    argparser.add_argument('project_path', metavar='PROJECT_PATH',
            help='project path')
    args = argparser.parse_args(sys.argv[1:])

    args.ignore = merge_ignores(
        args.ignore, read_ignore(
            find_ignore(args.project_path)
        )
    )

    if args.serve:
        server = Server(args.host, args.port, args)

        success('Starting up on %s:%s' % (args.host, args.port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            if not args.verbose:
                error('An exception occured, use `-v` if you want a traceback')
            else:
                error('An exception occured, traceback follows')
                traceback.print_exc(file=sys.stderr)

            sys.exit(1)
    else:
        project = parse(args.project_path, args.ignore)

        sys.stdout.write(
            html(project)
        )
