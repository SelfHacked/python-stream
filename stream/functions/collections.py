import typing as _typing

from returns import (
    returns as _returns,
)

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
    def __init__(
            self,
            index,
            *,
            none: bool = False,
    ):
        """
        :param none:
            If False (default), collections without index result in IndexError or KeyError;
            If True, fill with None instead.
        """
        self.__index = index
        self.__none = none

    @property
    def index(self):
        return self.__index

    @property
    def none(self) -> bool:
        return self.__none

    def _call(self, item: Collection) -> _typing.Any:
        try:
            return item[self.index]
        except (IndexError, KeyError):
            if not self.none:
                raise
            return None


class GetItems(_BaseOneToOneFunction[Collection, _typing.Tuple]):
    def __init__(
            self,
            *indexes,
            **kwargs,
    ):
        """
        :param kwargs: See GetItem
        """
        self.__get_items = [
            GetItem(index, **kwargs)
            for index in indexes
        ]

    @_returns(tuple)
    def _call(self, item: Collection) -> _typing.Tuple:
        for get_item in self.__get_items:
            yield get_item._call(item)


class ToDict(_BaseOneToOneFunction[_typing.Sequence, _typing.Dict]):
    def __init__(
            self,
            *keys,
            **kwargs,
    ):
        """
        :param kwargs: See GetItem
        """
        self.__get_items = [
            (key, GetItem(i, **kwargs))
            for i, key in enumerate(keys)
        ]

    @_returns(dict)
    def _call(self, item: _typing.Sequence) -> _typing.Dict:
        for key, get_item in self.__get_items:
            yield key, get_item._call(item)


class SelectKeys(_BaseOneToOneFunction[_typing.Mapping, _typing.Dict]):
    def __init__(
            self,
            *keys,
            **kwargs,
    ):
        """
        :param kwargs: See GetItem
        """
        self.__get_items = [
            GetItem(key, **kwargs)
            for key in keys
        ]

    @_returns(dict)
    def _call(self, item: _typing.Sequence) -> _typing.Dict:
        for get_item in self.__get_items:
            yield get_item.index, get_item._call(item)
