from typing import Any, Collection, Iterable, Iterator

from .each import BaseOneToOneFunction


def yield_from(iterable: Iterable[Iterable]) -> Iterator:
    """
    Unpack a series of iterables into one iterable.
    """
    for item in iterable:
        yield from item


class getitem(BaseOneToOneFunction[Collection, Any]):
    def __init__(self, index):
        self.__index = index

    def _call(self, item):
        return item[self.__index]
