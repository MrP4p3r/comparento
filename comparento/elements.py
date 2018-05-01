# -*- coding: utf-8 -*-

from . import constants
from . import operands
from . import expander


class Element(expander.Expandable):
    pass


class Symbol(Element, operands.MathOperand, operands.ComparisonOperand):

    _expand_name_ = 'symbol'

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class SymbolExpression(Element):

    _expand_name_ = 'symbol_expression'

    def __init__(self, operator, symbol):
        self.operator = operator
        self.symbol = symbol


class Expression(Element):

    # __new__ as factory for MathExpression and BooleanExpression

    def __init__(self, operator, operands_lst):
        self.operator = operator
        self.operands = self.flatten(operands_lst)

    def flatten(self, elements):
        new_elements_list = []
        for operand in elements:
            if isinstance(operand, self.__class__) and operand.operator == self.operator:
                new_elements_list.extend(operand.operands)
            else:
                new_elements_list.append(operand)
        return new_elements_list

    def __repr__(self):
        op_repr = f' {constants.operator_repr[self.operator]} '

        def _add_brackets(operand):
            if hasattr(operand, 'operator') and constants.cmp_operator_priority(self, operand) > 0:
                return f'({repr(operand)})'
            return repr(operand)

        return op_repr.join(map(_add_brackets, self.operands))


class MathExpression(Expression, operands.MathOperand, operands.ComparisonOperand):

    _expand_name_ = 'math_expression'


class BooleanExpression(Expression, operands.BooleanOperand):

    _expand_name_ = 'boolean_expression'


class Comparison(Element, operands.BooleanOperand):

    _expand_name_ = 'comparison'

    def __init__(self, operator, one, two):
        self.one = one
        self.two = two
        self.operator = operator

    def __repr__(self):
        return f'{self.one!r} {constants.operator_repr[self.operator]} {self.two!r}'
