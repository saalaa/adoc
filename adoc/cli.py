"""Command-line interface.

This module exports the program's entry point: `main`.
"""

import argparse
import colorlog
import logging
import sys

from .errors import FatalError
from .httpd import Server
from .parser import ProjectParser
from .version import version
from .writers import find_writer

logger = logging.getLogger(__name__)


class SplitAppend(argparse.Action):
    """Argument parsing action for repeatable csv strings."""
    def __call__(self, parser, namespace, values, option_string=None):
        old_value = getattr(namespace, self.dest) or []
        new_value = old_value + values.split(',')

        setattr(
            namespace, self.dest, new_value
        )


def cli_setup():
    """CLI arguments parser setup."""
    ap = argparse.ArgumentParser(
        prog='adoc', description='A Python documentation generation tool'
    )

    ap.add_argument('project_path', metavar='PROJECT_PATH',
                    help='project path')

    ap.add_argument('--version', action='version',
                    version='%(prog)s ' + version)

    ap.add_argument('-v', '--verbose', action='store_true',
                    help='run in verbose mode')

    group = ap.add_argument_group('output control')

    group.add_argument('--http', type=str, help='HTTP live server')

    group.add_argument('--html', type=str, help='HTML output file')
    group.add_argument('--md', type=str, help='Markdown output file')
    group.add_argument('--pdf', type=str, help='PDF output file')

    group = ap.add_argument_group('configuration')

    group.add_argument('-d', '--documents', type=str, action=SplitAppend,
                       help='additional documentation')

    group.add_argument('-f', '--docstrings-format', type=str, default='md',
                       help='docstrings format (`md` or `rst`)')

    group.add_argument('--strip-docstrings', action='store_true',
                       help='strip docstrings off of embedded YAML documents')

    group.add_argument('--no-setup', action='store_true',
                       help='disable parsing of `setup.py`')

    group.add_argument('--find-packages', action='store_true',
                       help='force-find packages using setuptools')

    group.add_argument('-x', '--exclude', type=str, action=SplitAppend,
                       help='set excluded packages')

    group = ap.add_argument_group('setup.py overrides')

    group.add_argument('--project-name', type=str,
                       help='override project name')

    group.add_argument('--project-version', type=str,
                       help='override project version')

    group.add_argument('-s', '--scripts', type=str, action=SplitAppend,
                       help='override scripts')

    group.add_argument('--package-dir', type=str,
                       help='override package directory')

    group.add_argument('-p', '--packages', type=str, action=SplitAppend,
                       help='override packages')

    return ap


def cli_compat(ap):
    """CLI backward compatibility."""
    def warning(old_flag, new_flag):
        logger.warning(
            '`{}` is deprecated, use `{}` instead'.format(old_flag, new_flag)
        )

        return 1

    def _cli_compat(args):
        warnings = 0

        if args.output:
            warnings += warning('-o, --output', '--html')
            args.html = args.output

        if args.rst_docstrings:
            warnings += warning('--rst-docstrings', '--docstrings-format')
            args.docstrings_format = 'rst'

        if args.serve:
            warnings += warning('--serve', '--http')
            args.http = ':'

        if args.host:
            warnings += warning('--host', '--http-host')
            args.http = args.host + ':'

        if args.port:
            warnings += warning('--port', '--http-port')
            args.http = ':' + args.port

        if warnings:
            logger.warning(
                'support for deprecated flags will be dropped soon'
            )

        return args

    suppress = dict(help=argparse.SUPPRESS)

    ap.add_argument('-o', '--output', type=str, **suppress)
    ap.add_argument('--rst-docstrings', action='store_true', **suppress)
    ap.add_argument('--serve', action='store_true', **suppress)
    ap.add_argument('--host', type=str, **suppress)
    ap.add_argument('--port', type=int, **suppress)

    return _cli_compat


def logging_setup(verbose):
    format = '%(log_color)s%(message)s%(reset)s'

    if verbose:
        format = '%(log_color)s%(levelname)s%(reset)s %(name)s %(message)s'

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            format
        )
    )

    logger = colorlog.getLogger()
    logger.addHandler(handler)

    logging.getLogger().setLevel(
        logging.DEBUG if verbose else logging.INFO
    )


def main(args=None):
    """Program entry point.

    This is where command line arguments are configured and read. Then the
    configuration is fine-tuned for execution.
    """
    ap = cli_setup()
    args = cli_compat(ap)(
        ap.parse_args(args or sys.argv[1:])
    )

    logging_setup(args.verbose)

    metadata = {}

    if args.project_name:
        metadata['name'] = args.project_name

    if args.project_version:
        metadata['version'] = args.project_version

    if args.scripts:
        metadata['scripts'] = args.scripts

    if args.package_dir:
        metadata['package_dir'] = {
            '': args.package_dir
        }

    if args.packages:
        metadata['packages'] = args.packages

    parser = ProjectParser(
        args.project_path,
        metadata,
        no_setup=args.no_setup,
        find_packages=args.find_packages,
        exclude=args.exclude,
        documents=args.documents
    )

    if not args.http and not args.html and not args.md and not args.pdf:
        logger.error(
            'no output specified, use `--http`, `--html`, `--md` or `--pdf`'
        )

        return 1

    docstrings_format = args.docstrings_format
    strip_docstrings = args.strip_docstrings

    if args.http:
        try:
            host, port = args.http.split(':')

            host = host or '127.0.0.1'
            port = int(
                port or '8080'
            )
        except Exception:
            logger.error(
                'value for `--http` must a be host-port combination: `:8080`'
            )

            return 1

        server = Server(
            host, port, parser, docstrings_format, strip_docstrings
        )

        logger.info(
            'server live at http://{}:{}'.format(
                host, port
            )
        )

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            return 0
        except Exception:
            logger.exception('uncaught exception')
            return 1
    else:
        filename = args.html or args.md or args.pdf

        project = parser.parse()
        writer = find_writer(args)

        try:
            writer(
                filename, project, docstrings_format, strip_docstrings
            )
        except FatalError as err:
            return err.log(return_with=1)

        logger.info(
            'written {}'.format(filename)
        )

        return 0
