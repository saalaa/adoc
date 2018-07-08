# **adoc** project

This program generates HTML documentation for Python projects by parsing the
source code using Python's AST module. As such the source code is *not* loaded,
it never reaches the interpreter and side-effects are effortlessly avoided.

Current target is to support Python 3.5 and above.


## Installation

There is no release available yet. At this point, the project is essentially a
preview.

The only way to test this project is through clone this repository and
preparing a virtual environment for it:

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt


## Usage

To start a web server for this project:

    python -m adoc http .

To generate this project's documentation:

    python -m adoc html . > adoc.html
