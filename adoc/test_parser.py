from .parser import parse
from .writer import html
from .ignores import (
    merge_ignores, find_ignore, read_ignore
)


def test_parse(capsys):
    project_path = '.'
    ignore = merge_ignores(
        read_ignore(
            find_ignore(project_path)
        )
    )

    project = parse(
        project_path, ignore
    )

    assert project

    assert 'Project' in str(project)

    assert 9 == len(
        project.iter_modules()
    )

    assert 19 == len(
        project.iter_functions()
    )

    assert 12 == len(
        project.iter_classes()
    )

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out

    assert '<!doctype html>' in html(project)
