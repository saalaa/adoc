import tempfile

from adoc.cli import main


def test_django_project(capsys):
    with tempfile.NamedTemporaryFile() as file:
        exit_status = main(
            ['-o', file.name, 'examples/django-project']
        )

    assert exit_status == 0

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out


def test_appengine_project(capsys):
    with tempfile.NamedTemporaryFile() as file:
        exit_status = main(
            ['--scripts', 'main.py', '-o', file.name,
                'examples/appengine-project']
        )

    assert exit_status == 0

    cap = capsys.readouterr()

    assert not cap.err
    assert not cap.out
