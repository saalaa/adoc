"""Python source code generation."""

import ast
import logging

logger = logging.getLogger(__name__)


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

COMPARE_OP_MAPPING = {
    ast.Eq: '==',
    ast.NotEq: '!=',
    ast.Lt: '<',
    ast.LtE: '<=',
    ast.Gt: '>',
    ast.GtE: '>=',
    ast.Is: 'is',
    ast.IsNot: 'is not',
    ast.In: 'in',
    ast.NotIn: 'not in'
}

BOOL_OP_MAPPING = {
    ast.And: 'and',
    ast.Or: 'or'
}


def lookup(mapping, atom):
    return mapping.get(
        type(atom), '???'
    )


def make_signature(node):
    items = []

    padding = [None] * (len(node.args) - len(node.defaults))

    for arg, default in zip(node.args, padding + node.defaults):
        if not default:
            items.append(arg.arg)
        else:
            default = make_python(default)

            items.append(
                '{}={}'.format(arg.arg, default)
            )

    if node.vararg:
        items.append(
            '*{}'.format(node.vararg.arg)
        )

    if node.kwarg:
        items.append(
            '**{}'.format(node.kwarg.arg)
        )

    return items


def make_python(node):
    """Generate Python code from an AST node (a subtree).
    """
    if node is None:
        return '!!!'
    elif isinstance(node, ast.Num):
        return '{}'.format(node.n)
    elif isinstance(node, ast.Str):
        return repr(node.s)
    elif isinstance(node, ast.Bytes):
        return "b'...'"
    elif isinstance(node, ast.NameConstant):
        return repr(node.value)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return '{}.{}'.format(
            make_python(node.value), node.attr
        )
    elif isinstance(node, ast.Tuple):
        items = [
            make_python(element) for element in node.elts
        ]

        if len(items) == 1:
            items.append('')

        return '({})'.format(
            ', '.join(items)
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

        return '{{{}}}'.format(
            ', '.join(items)
        )
    elif isinstance(node, ast.Dict):
        items = [
            '{}: {}'.format(make_python(key), make_python(value))
            for key, value in zip(node.keys, node.values)
        ]

        return '{{{}}}'.format(
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
    elif isinstance(node, ast.Lambda):
        return 'lambda {}: {}'.format(
            make_python(node.args), make_python(node.body)
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
    elif isinstance(node, ast.Compare):
        items = [
            make_python(node.left)
        ]

        for op, right in zip(node.ops, node.comparators):
            items.append(
                lookup(COMPARE_OP_MAPPING, op)
            )
            items.append(
                make_python(right)
            )

        return ' '.join(items)
    elif isinstance(node, ast.BoolOp):
        items = []
        for idx, value in enumerate(node.values):
            if idx:
                items.append(
                    lookup(BOOL_OP_MAPPING, node.op)
                )

            items.append(
                make_python(value)
            )

        return '({})'.format(
            ' '.join(items)
        )
    elif isinstance(node, ast.arguments):
        return ', '.join(
            make_signature(node)
        )

    logger.error(
        'unsupported node: {}'.format(node)
    )

    return '???'
