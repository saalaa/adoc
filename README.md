[![Build Status](https://travis-ci.org/saalaa/adoc.svg?branch=master)](https://travis-ci.org/saalaa/adoc)

# **adoc** project

This program generates HTML documentation for Python projects by parsing the
source code using Python's AST module. As such the source code is *not* loaded,
it never reaches the interpreter and side-effects are effortlessly avoided.

This projet targets Python 3.5 and above.


## Features

- AST-based Python parsing
- Fully `setup.py` -based configuration
- Markdown and RST support
- Built-in HTTP live-server
- Single HTML artifact


## Long-term Goals

- Symbol resolution, allowing linking through symbols within the document
- Arbitrary Markdown files inclusion, creating new sections as needed
- Provide graceful support for common Sphinx directives
- JPEG/PNG media inclusion (only one final artifact)


## CLI

The following command line arguments are supported:

- `--rst-docstrings`: format docstrings using RST
- `--no-setup`: disable parsing of `setup.py`
- `--name NAME`: override project name
- `--version VERSION`: override project version
- `--package-dir PACKAGE_DIR`: override package directory
- `--packages PACKAGES`: override packages
- `--find-packages`: force-find packages using setuptools
- `--exclude EXCLUDE`: set excluded packages
- `--serve`: serve documentation over HTTP
- `--host HOST`: live-server host, defaults to 0.0.0.0
- `--port PORT`: live-server port, defaults to 8080

A positional argument is also necessary, indicating the path to the project.


## Installation

There is no release available yet. At this point, the project is essentially a
preview.

The only way to test this project is through cloning this repository and
preparing a virtual environment for it:

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt


## Usage

To start a web server for this project:

    python -m adoc --serve .

To generate this project's documentation:

    python -m adoc html . > adoc.html
