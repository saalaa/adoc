"""Python source code generation."""

import ast

from .utils import warning

BINARY_OP_MAPPING = {
    ast.Add: '+',
    ast.BitAnd: '&',
    ast.BitOr: '|',
    ast.BitXor: '^',
    ast.Div: '/',
    ast.FloorDiv: '//',
    ast.LShift: '<<',
    ast.Mod: '%',
    ast.Mult: '*',
    ast.Pow: '**',
    ast.RShift: '>>',
    ast.Sub: '-'
}

UNARY_OP_MAPPING = {
    ast.Invert: '~',
    ast.Not: 'not',
    ast.UAdd: '+',
    ast.USub: '-'
}


def lookup(mapping, atom):
    return mapping.get(
        type(atom), '???'
    )


def make_python(node):
    """Generate Python code from an AST node (a subtree).
    """
    if node is None:
        return ''
    elif isinstance(node, ast.Num):
        return '{}'.format(node.n)
    elif isinstance(node, ast.Str):
        return repr(node.s)
    elif isinstance(node, ast.Bytes):
        return "b'...'"
    elif isinstance(node, ast.NameConstant):
        return '{}'.format(node.value)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return '{}.{}'.format(
            make_python(node.value), node.attr
        )
    elif isinstance(node, ast.List):
        items = [
            make_python(element) for element in node.elts
        ]

        return '[{}]'.format(
            ', '.join(items)
        )
    elif isinstance(node, ast.Set):
        items = [
            make_python(element) for element in node.elts
        ]

        return '[{}]'.format(
            ', '.join(items)
        )
    elif isinstance(node, ast.Call):
        items = []

        for arg in node.args:
            items.append(
                make_python(arg)
            )

        for keyword in node.keywords:
            items.append(
                '{}={}'.format(
                    keyword.arg, make_python(keyword.value)
                )
            )

        return '{}({})'.format(
            make_python(node.func), ', '.join(items)
        )
    elif isinstance(node, ast.UnaryOp):
        return '{}{}'.format(
            lookup(UNARY_OP_MAPPING, node.op),
            make_python(node.operand)
        )
    elif isinstance(node, ast.BinOp):
        return '{} {} {}'.format(
            make_python(node.left),
            lookup(BINARY_OP_MAPPING, node.op),
            make_python(node.right)
        )

    warning(
        'Unknown node: {}'.format(node)
    )

    return '???'
