# **adoc** project

This program generates HTML documentation for Python projects by parsing the source code using
Python's AST module. As such the source code is *not* loaded, it never reaches the interpreter and
side-effects are effortlessly avoided.

## Installation

    pip install adoc

## Usage

To generate this project's documentation:

    adoc html . > adoc.html

To start a web server for this project:

    adoc http .

Or:

    #!python
    for item in range(666):
        print(item)

sxx

    #!python
    >>> def test():
    ...     '''This is a docstring.'''
    ...     pass
    ...
    >>> test.__doc__
    'This is a docstring.'

