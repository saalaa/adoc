"""Command-line interface.

This module provides CLI-related functionalities such as the various commands,
arguments/options parsing and live CLI documentation.

Since *docstrings* are used to provide live CLI documentation and may thus
sound slightly out of tone.

This module also exports the program's entrypoint: `main`.
"""
import sys
import click
import traceback

# from .models import walk
from .parser import parse
from .writer import html
from .utils import error, success
from .httpd import Server


project_type = click.Path(exists=True, readable=True, resolve_path=True,
        file_okay=False)


@click.group()
def main():
    """A Python documentation generation tool."""
    pass


@main.command('html')
@click.option('--verbose', '-v', is_flag=True)
@click.option('--output', '-o', default='-')
@click.argument('project_path', type=project_type)
def html_command(verbose, output, project_path):
    """Render documentation as an HTML document.
    """
    try:
        project = parse(project_path)
    except:
        if not verbose:
            error('An exception occured, use `-v` if you want a traceback')
        else:
            error('An exception occured, traceback follows')
            click.echo(
                traceback.format_exc(), err=True
            )

        sys.exit(1)

    if output == '-':
        output = sys.stdout
    else:
        output = open(output, 'w')

    click.echo(
        html(project), file=output
    )


@main.command('http')
@click.option('--verbose', '-v', is_flag=True)
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', default=8080, type=int)
@click.argument('project_path', type=project_type)
def http_command(verbose, host, port, project_path):
    """Serve HTML documentation over HTTP.
    """
    server = Server(host, port, project_path)

    success('Starting up on %s:%s' % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        if not verbose:
            error('An exception occured, use `-v` if you want a traceback')
        else:
            error('An exception occured, traceback follows')
            click.echo(
                traceback.format_exc(), err=True
            )

        sys.exit(1)
