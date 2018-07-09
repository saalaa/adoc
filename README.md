[![Build Status](https://travis-ci.org/saalaa/adoc.svg?branch=master)](https://travis-ci.org/saalaa/adoc)

# **adoc** project

This program generates HTML documentation for Python projects by parsing the
source code using Python's AST module. As such the source code is *not* loaded,
it never reaches the interpreter and side-effects are effortlessly avoided.

This projet targets Python 3.5 and above.


# Features

- Reads common *ignore* files
- AST-based Python parsing
- Ability to start an HTTP server (rebuild on reload)
- Markdown support
- Single HTML artifact


## Short-term Goals

- Test suite (esp. metaclasses)
- More documentation
- Release a proper package


## Long-term Goals

- Code cleanup, it's kind of thrown together right now
- Symbol resolution, allowing linking through symbols within the document
- Arbitrary Markdown files inclusion, creating new sections as needed
- JPEG/PNG media inclusion (only one final artifact)
- Project information sniffing (license, project URL, CI jobs, etc...)
- Support both Markdown and ReStructuredText


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
