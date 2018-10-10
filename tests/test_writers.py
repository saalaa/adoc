import pytest
import tempfile

from adoc.errors import FatalError
from adoc.parser import ProjectParser
from adoc.writers import (
    write_html, write_md, write_pdf
)


def test_html_md(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    with tempfile.NamedTemporaryFile(mode='w+') as fh:
        write_html(fh.name, project, 'md', False)

        assert '<!doctype html>' in fh.read()

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_html_rst(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    with tempfile.NamedTemporaryFile(mode='w+') as fh:
        write_html(fh.name, project, 'rst', False)

        assert '<!doctype html>' in fh.read()

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_md_md(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    with tempfile.NamedTemporaryFile(mode='w+') as fh:
        write_md(fh.name, project, 'md', False)

        assert 'API Reference' in fh.read()

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_md_rst(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    with tempfile.NamedTemporaryFile(mode='w+') as fh:
        with pytest.raises(FatalError, message='unsupported'):
            write_md(fh.name, project, 'rst', False)


def test_pdf_md(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    with tempfile.NamedTemporaryFile(mode='w+b') as fh:
        write_pdf(fh.name, project, 'md', False)

        assert fh.read().startswith(
            b'%PDF'
        )

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_pdf_rst(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    with tempfile.NamedTemporaryFile(mode='w+b') as fh:
        write_pdf(fh.name, project, 'rst', False)

        assert fh.read().startswith(
            b'%PDF'
        )

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out
