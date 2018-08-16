import tempfile

from adoc.cli import main


def test_django_project(capsys):
    with tempfile.NamedTemporaryFile() as file:
        exit_status = main(
            ['--html', file.name, 'examples/django-project']
        )

    assert exit_status == 0

    cap = capsys.readouterr()

    assert not cap.out
    assert 'written' in cap.err


def test_appengine_project(capsys):
    with tempfile.NamedTemporaryFile() as file:
        exit_status = main(
            ['-s', 'main.py', '--html', file.name,
             'examples/appengine-project']
        )

    assert exit_status == 0

    cap = capsys.readouterr()

    assert not cap.out
    assert 'written' in cap.err
