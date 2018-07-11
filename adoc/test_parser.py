from .parser import ProjectParser


def test_parse(capsys):
    parser = ProjectParser('.', {}, exclude=['*.tests', '*.tests.*', 'tests.*',
        'tests', 'test_*'])

    project = parser.parse()

    assert project

    assert 'Project' in str(project)

    assert 11 == len(
        project.iter_modules()
    )

    assert 15 == len(
        project.iter_functions()
    )

    assert 16 == len(
        project.iter_classes()
    )

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out
