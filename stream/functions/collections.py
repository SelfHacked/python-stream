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


Collection = _typing.Union[_typing.Sequence, _typing.Mapping]


class GetItem(_BaseOneToOneFunction[Collection, _typing.Any]):
    def __init__(self, index):
        self.__index = index

    def _call(self, item: Collection) -> _typing.Any:
        return item[self.__index]
