# FAQ


## I don't have a `setup.py`, what do I do?

Worry not. Although **adoc** will attempt to rely on `setup.py` as much as
possible, it will resort to *bare* `find_packages()` if it has to and there are
still command line overrides as well.

On a typical project, there wouldn't be any noticeable difference:

    adoc --serve .

However, you may be needed to adjust a couple of things:

    adoc --packages-dir=src --serve .

See `examples/django-project` and the corresponding [HTML
documentation](https://saalaa.github.io/adoc/django-project.html) to get an
idea.


## Why aren't my Python packages discovered properly?

**adoc** relies on either `setup.py` or `find_packages()` for package
discovery. If you have any issue, you may want to check these places first.

The result of `find_packages()` is easy to reproduce:

    >>> from setuptools import find_packages
    >>> find_packages('.')
    ['adoc', 'adoc.formats']

If a package appears missing even though it's a valid package, you'll probably
want to make sure it contains `__init__.py` since `find_packages()` relies on
these files to determine what is a package and what is not (even though they
are not required in recent Python versions).


## Why is one of my packages not showing up at all?

**adoc** is probably detecting that your package is empty. Here's the
definition of an empty package:

- Your package does not hold any *function*
- Your package does not hold any *class*
- Your package does not hold any *package*

That definition is recursive so that a package holding empty packages is
considered empty
