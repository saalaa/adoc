import ast
import textwrap

from .codegen import make_python


def test_unsupported(capsys):
    root = ast.parse(
        ''
    )

    assert make_python(None) == "!!!"
    assert make_python(root) == "???"

    assert 'unsupported' in capsys.readouterr().err.lower()

def test_function():
    source = '''
    def foo():
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == ""


def test_function_arg():
    source = '''
    def foo(bar):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "bar"


def test_function_default():
    source = '''
    def foo(bar='baz'):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "bar='baz'"


def test_function_default_lambda():
    source = '''
    def foo(bar=lambda x: x * 2):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "bar=lambda x: x * 2"


def test_function_default_comp():
    source = '''
    def foo(bar=('baz',) == b'asdf'):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "bar=('baz', ) == b'...'"


def test_function_varargs():
    source = '''
    def foo(*bar):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "*bar"


def test_function_kwargs():
    source = '''
    def foo(**bar):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "**bar"


def test_function_combined():
    source = '''
    def foo(foo, bar=[baz], *quux):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "foo, bar=[baz], *quux"


def test_function_decorators():
    source = '''
    @quux.okay
    @baz(True and False or {1, 2, 3})
    @bar(-1, 2.3, nope={True: None})
    def foo(bar, *baz, **quux):
        pass
    '''

    root = ast.parse(
        textwrap.dedent(source)
    )

    node = root.body[0]

    assert isinstance(node, ast.FunctionDef)
    assert make_python(node.args) == "bar, *baz, **quux"
    assert make_python(node.decorator_list[0]) == "quux.okay"
    assert make_python(node.decorator_list[1]) == "baz(((True and False) or {1, 2, 3}))"
    assert make_python(node.decorator_list[2]) == "bar(-1, 2.3, nope={True: None})"
