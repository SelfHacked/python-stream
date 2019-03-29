import typing as _typing

from .each import (
    BaseOneToOneFunction as _BaseOneToOneFunction,
)


def yield_from(iterable: _typing.Iterable[_typing.Iterable]) -> _typing.Iterator:
    """
    Unpack a series of iterables into one iterable.
    """
    for item in iterable:
        yield from item


class getitem(_BaseOneToOneFunction[_typing.Collection, _typing.Any]):
    def __init__(self, index):
        self.__index = index

    def _call(self, item):
        return item[self.__index]
