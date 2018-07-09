import click

from functools import wraps


def success(message):
    click.echo(
        click.style('Success: ', fg='green') + message
    )


def warning(message):
    click.echo(
        click.style('Warning: ', fg='yellow') + message, err=True
    )


def error(message):
    click.echo(
        click.style('Error: ', fg='red') + message, err=True
    )


def memoized(f):
    f._cache = {}

    @wraps(f)
    def wrapper(*args, **kwargs):
        if args in f._cache:
            return f._cache[args]

        value = f(*args, **kwargs)

        f._cache[args] = value

        return value

    return wrapper
