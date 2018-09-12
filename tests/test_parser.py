from adoc.parser import ProjectParser


def test_parse(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    assert 'Project' in str(project)

    assert 14 == len(
        project.iter_modules()
    )

    assert 16 == len(
        project.iter_functions()
    )

    assert 19 == len(
        project.iter_classes()
    )

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out
