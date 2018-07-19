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
