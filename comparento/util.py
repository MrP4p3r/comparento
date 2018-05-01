# -*- coding: utf-8 -*-

import inspect


def cmp(a, b):
    x = a - b
    return x / abs(x) if x != 0 else 0


class FallbackDict(dict):

    def __init__(self, dct, fallback):
        super().__init__(dct)
        self._fallback = fallback

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        return self._fallback[key]


class BetterDefaultDict(dict):
    """Альтернатива collections.defaultdict.
    Учитывает сигнатуру `default_factory`. Если фабрика не принимает
    аргументов, работает как и defaultdict. Если принимает один, передается ключ элемента.

    >>> d = BetterDefaultDict(lambda key: str(key)+'Value')
    >>> d['hello']
    'helloValue'

    """

    def __init__(self, default_factory):
        """
        :param callable default_factory:
        """
        default_factory_argcount = len(inspect.signature(default_factory).parameters)
        if default_factory_argcount == 0:
            self.default_factory = lambda x: default_factory()
        elif default_factory_argcount == 1:
            self.default_factory = default_factory
        else:
            raise TypeError('Bad signature for default_factory. Allowed signatures are (any) -> any OR () -> any')

    def __getitem__(self, key):
        if key not in self:
            self[key] = self.default_factory(key)
        return super().__getitem__(key)
