# -*- coding: utf-8 -*-

import operator as op
from functools import reduce

from . import util


class ExpandableMeta(type):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        _create_expand_fn(cls)


def _create_expand_fn(cls):
    if cls.__name__ == 'Expandable':
        return

    name = getattr(cls, '_expand_name_', None)
    if name is None:
        return

    get_expander = op.attrgetter(f'expand_{name}')

    def expand(self, tr):
        return get_expander(tr)(self)

    setattr(cls, 'expand', expand)


class Expandable(object, metaclass=ExpandableMeta):

    _expand_name_ = None


class ExpressionExpander(object):

    def __init__(self,
                 symbol_table,
                 expand_literal=lambda tr, x: x,
                 operator_fn_table=None,
                 operator_aggr_fn_table=None):
        """

        :param dict[str, any] symbol_table:
            Symbol evaluations by symbol names.

        :param (ExpressionExpander, any) -> any expand_literal:
            Literal expander function.

        :param dict[str, (any, any) -> any] operator_fn_table:
            Operator functions by operator names.

        :param dict[str, (list[any]) -> any] operator_aggr_fn_table:
            Aggregative operator functions by operator names.
            Expands to reduce based function by default. In this case it uses `operator_fn_table`.

        """

        self.symbol_table = symbol_table
        self.expand_literal = expand_literal

        # operator function table
        default_operator_fn_table = util.BetterDefaultDict(lambda operator_name: getattr(op, operator_name))
        if operator_fn_table:
            self.operator_functions = util.FallbackDict(operator_fn_table, fallback=default_operator_fn_table)
        else:
            self.operator_functions = default_operator_fn_table

        # aggregative operator functions table
        default_operator_aggr_fn_table = util.BetterDefaultDict(
            lambda operator_name: create_aggr_operator_fn(self, operator_name)
        )
        if operator_aggr_fn_table:
            self.operator_aggr_fn_table = util.FallbackDict(operator_aggr_fn_table, fallback=default_operator_fn_table)
        else:
            self.operator_aggr_fn_table = default_operator_aggr_fn_table

    def expand(self, expr):
        method = getattr(expr, 'expand', None)
        if method:
            return method(self)
        return self.expand_literal(self, expr)

    def expand_boolean_expression(self, expr):
        """
        :param comparento.BooleanExpression expr:
        """
        sub_exprs = list(map(self.expand, expr.operands))
        result = self.operator_aggr_fn_table[expr.operator](sub_exprs)
        return result

    def expand_comparison(self, expr):
        """
        :param comparento.Comparison expr:
        """
        return self.operator_functions[expr.operator](self.expand(expr.one), self.expand(expr.two))

    def expand_math_expression(self, expr):
        """
        :param comparento.MathExpression expr:
        """
        sub_exprs = list(map(self.expand, expr.operands))
        return self.operator_aggr_fn_table[expr.operator](sub_exprs)

    def expand_symbol_expression(self, expr):
        """
        :param comparento.SymbolExpression expr:
        """
        self.operator_functions[expr.operator](self.expand(expr.symbol))

    def expand_symbol(self, expr):
        """
        :param comparento.Symbol expr:
        """
        return self.symbol_table[expr.name]


def create_aggr_operator_fn(tr, operator_name):
    op_fn = tr.operator_functions[operator_name]
    return lambda expr_lst: reduce(op_fn, expr_lst[1:], expr_lst[0])
