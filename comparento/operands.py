# -*- coding: utf-8 -*-

from . import elements


class UnaryOperand:

    def handle_unary_operator(self, operator):
        return elements.SymbolExpression(operator, self)

    def __neg__(self):
        return self.handle_unary_operator('__neg__')


class MathOperand:

    def handle_math_operator(self, operator, other):
        return elements.MathExpression(operator, [self, other])

    def __add__(self, other):
        return self.handle_math_operator('__add__', other)

    def __sub__(self, other):
        return self.handle_math_operator('__sub__', other)

    def __mul__(self, other):
        return self.handle_math_operator('__mul__', other)

    def __truediv__(self, other):
        return self.handle_math_operator('__truediv__', other)

    def __floordiv__(self, other):
        return self.handle_math_operator('__floordiv__', other)

    def __pow__(self, power):
        return self.handle_math_operator('__pow__', power)


class ComparisonOperand:

    def handle_comparison_operator(self, operator, other):
        return elements.Comparison(operator, self, other)

    def __eq__(self, other):
        self.handle_comparison_operator('__eq__', other)

    def __ne__(self, other):
        return self.handle_comparison_operator('__ne__', other)

    def __gt__(self, other):
        return self.handle_comparison_operator('__gt__', other)

    def __ge__(self, other):
        return self.handle_comparison_operator('__ge__', other)

    def __lt__(self, other):
        return self.handle_comparison_operator('__lt__', other)

    def __le__(self, other):
        return self.handle_comparison_operator('__le__', other)


class BooleanOperand:

    def handle_boolean_operator(self, operator, other):
        return elements.BooleanExpression(operator, [self, other])

    def __and__(self, other):
        return self.handle_boolean_operator('__and__', other)

    def __or__(self, other):
        return self.handle_boolean_operator('__or__', other)
