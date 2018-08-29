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
from .writer import html

# TODO Try to merge --http-host and --http-port into --http before release
# TODO Rework writer module and implement --pdf

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

    ap.add_argument('--version', action='version',
                    version='%(prog)s ' + version)

    ap.add_argument('-v', '--verbose', action='store_true',
                    help='run in verbose mode')

    ap.add_argument('--html', type=str,
                    help='HTML output file')

    # ap.add_argument('--pdf', type=str,
    #                 help='PDF output file')

    ap.add_argument('--http', action='store_true',
                    help='serve documentation over HTTP')

    ap.add_argument('--http-host', type=str, default='0.0.0.0',
                    help='HTTP host, defaults to 0.0.0.0')

    ap.add_argument('--http-port', type=int, default='8080',
                    help='HTTP port, defaults to 8080')

    ap.add_argument('-d', '--documents', type=str, action=SplitAppend,
                    help='additional documentation')

    ap.add_argument('-f', '--docstrings-format', type=str, default='md',
                    help='docstrings format (`md` or `rst`)')

    ap.add_argument('--no-setup', action='store_true',
                    help='disable parsing of `setup.py`')

    ap.add_argument('--project-name', type=str,
                    help='override project name')

    ap.add_argument('--project-version', type=str,
                    help='override project version')

    ap.add_argument('-s', '--scripts', type=str, action=SplitAppend,
                    help='override scripts')

    ap.add_argument('--package-dir', type=str,
                    help='override package directory')

    ap.add_argument('-p', '--packages', type=str, action=SplitAppend,
                    help='override packages')

    ap.add_argument('--find-packages', action='store_true',
                    help='force-find packages using setuptools')

    ap.add_argument('-x', '--exclude', type=str, action=SplitAppend,
                    help='set excluded packages')

    ap.add_argument('project_path', metavar='PROJECT_PATH',
                    help='project path')

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
            args.http = True

        if args.host:
            warnings += warning('--host', '--http-host')
            args.http_host = args.host

        if args.port:
            warnings += warning('--port', '--http-port')
            args.http_port = args.port

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

    if args.http:
        server = Server(args.http_host, args.http_port, parser,
                        args.docstrings_format)

        logger.info(
            'server live at http://{}:{}'.format(
                args.http_host, args.http_port
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
        filename = args.html  # or args.pdf

        if not filename:
            logger.error('no output format specified, use `--html`')
            return 1

        project = parser.parse()

        try:
            output = html(project, args.docstrings_format)
        except FatalError as err:
            return err.log(return_with=1)

        with open(filename, 'w') as fh:
            fh.write(
                output
            )

        logger.info(
            'written {}'.format(filename)
        )

        return 0
