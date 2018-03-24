# -*- coding: utf-8 -*-


operator_repr = {
    # math
    '__add__': '+',
    '__sub__': '-',
    '__mul__': '*',
    '__truediv__': '/',
    '__floordiv__': '//',
    '__pow__': '**',

    # comparisons
    '__ne__': '!=',
    '__eq__': '==',
    '__gt__': '>',
    '__ge__': '>=',
    '__lt__': '<',
    '__le__': '<=',

    # logic
    '__or__': 'OR',
    '__and__': 'AND',
    '__xor__': 'XOR',
}


operator_priority = {
    # math
    '__add__': 1000,
    '__sub__': 1000,
    '__mul__': 1050,
    '__truediv__': 1050,
    '__floordiv__': 1050,
    '__pow__': 1100,

    # comparison
    '__ne__': 700,
    '__eq__': 700,
    '__gt__': 700,
    '__ge__': 700,
    '__lt__': 700,
    '__le__': 700,

    # logic
    '__or__': 500,
    '__xor__': 500,
    '__and__': 550,
}