# -*- coding: utf-8 -*-

from . import constants


def cmp(a, b):
    x = a - b
    return x / abs(x) if x != 0 else 0


def cmp_operator_priority(one, two):
    return cmp(constants.operator_priority[one.operator], constants.operator_priority[two.operator])
