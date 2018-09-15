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
- Single HTML, PDF or Markdown artifact


## Long-term Goals

- Symbol resolution, allowing linking through symbols within the document
- JPEG/PNG media inclusion (only one final artifact)
- In-document Graphviz processing


## Installation

This is fairly straighforward:

    pip install adoc


## Usage

For iteractive generation:

    adoc --http .

For an HTML export:

    adoc --html docs/index.html .


## Hacking on the project

Prepare a virtual environment:

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    pip install -r requirements-pdf.txt
    pip install -r requirements-test.txt

Run the test suite:

    pytest .

To start the web server:

    python -m adoc --http .
