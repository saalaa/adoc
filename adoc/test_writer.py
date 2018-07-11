from .parser import ProjectParser
from .writer import html


def test_html_md(capsys):
    parser = ProjectParser('.', {}, exclude=['*.tests', '*.tests.*', 'tests.*',
        'tests', 'test_*'])

    project = parser.parse()

    assert project

    assert '<!doctype html>' in html(project, 'md')

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_html_rst(capsys):
    parser = ProjectParser('.', {}, exclude=['*.tests', '*.tests.*', 'tests.*',
        'tests', 'test_*'])

    project = parser.parse()

    assert project

    assert '<!doctype html>' in html(project, 'rst')

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out
