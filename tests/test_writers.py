import pytest

from adoc.errors import FatalError
from adoc.parser import ProjectParser
from adoc.writers import (
    write_html, write_md
)


def test_html_md(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    assert '<!doctype html>' in write_html(project, 'md')

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_html_rst(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    assert '<!doctype html>' in write_html(project, 'rst')

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_md_md(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    assert 'API Reference' in write_md(project, 'md')

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_md_rst(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    with pytest.raises(FatalError, message='unsupported'):
        write_md(project, 'rst')
