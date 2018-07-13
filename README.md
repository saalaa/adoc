[![Build Status](https://travis-ci.org/saalaa/adoc.svg?branch=master)](https://travis-ci.org/saalaa/adoc)

# **adoc** project

This program generates HTML documentation for Python projects by parsing the
source code using Python's AST module. As such the source code is *not* loaded,
it never reaches the interpreter and side-effects are effortlessly avoided.

This projet targets Python 3.5 and above.


## Features

- AST-based Python parsing
- Fully `setup.py` -based configuration
- MD/RST docstrings support
- Additional files inclusion as separate doc sections
- Built-in HTTP live-server
- Single HTML artifact


## Installation

This is fairly straighforward:

    pip install adoc


## CLI

The following command line arguments are supported:

    positional arguments:
      PROJECT_PATH          project path

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -v                    run in verbose mode
      -o OUTPUT, --output OUTPUT
                            output file
      -d DOCUMENT           additional document
      --rst-docstrings      format docstrings using RST
      --no-setup            disable parsing of `setup.py`
      --project-name PROJECT_NAME
                            override project name
      --project-version PROJECT_VERSION
                            override project version
      --package-dir PACKAGE_DIR
                            override package directory
      --packages PACKAGES   override packages
      --find-packages       force-find packages using setuptools
      --exclude EXCLUDE     set excluded packages
      --serve               serve documentation over HTTP
      --host HOST           live-server host, defaults to 0.0.0.0
      --port PORT           live-server port, defaults to 8080


Sample usage:

    adoc --serve .
    adoc -o docs/index.html .


## Long-term Goals

- Symbol resolution, allowing linking through symbols within the document
- JPEG/PNG media inclusion (only one final artifact)
- In-document Graphviz processing


## Hacking on the project

Prepare a virtual environment:

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements-test.txt

Run the test suite:

    pytest .

To start the web server:

    python -m adoc --serve .
