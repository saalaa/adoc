from adoc.parser import ProjectParser


def test_parse(capsys):
    parser = ProjectParser('.', {})
    project = parser.parse()

    assert project

    assert 'Project' in str(project)

    assert 15 == len(
        project.iter_modules()
    )

    assert 21 == len(
        project.iter_functions()
    )

    assert 20 == len(
        project.iter_classes()
    )

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out
