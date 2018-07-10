from .parser import ProjectParser
from .writer import html


def test_parse(capsys):
    project_path = '.'

    parser = ProjectParser(project_path, {}, exclude=['*.tests', '*.tests.*',
        'tests.*', 'tests', 'test_*'])

    project = parser.parse()

    assert project

    assert 'Project' in str(project)

    assert 8 == len(
        project.iter_modules()
    )

    assert 12 == len(
        project.iter_functions()
    )

    assert 14 == len(
        project.iter_classes()
    )

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out

    assert '<!doctype html>' in html(project)
