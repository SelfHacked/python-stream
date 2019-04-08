import typing as _typing

from stream.typing import (
    Function as _Function,
    T_co as _T_co,
)


class BaseFilter(_Function[_T_co, _T_co]):
    def _match(self, item) -> bool:
        raise NotImplementedError  # pragma: no cover

    def __call__(self, iterable: _typing.Iterable[_T_co]) -> _typing.Iterator[_T_co]:
        for item in iterable:
            if not self._match(item):
                continue
            yield item

    def __invert__(self):
        return Filter(lambda item: not self._match(item))

    def __and__(self, other: 'BaseFilter'):
        return Filter(lambda item: self._match(item) and other._match(item))

    def __or__(self, other: 'BaseFilter'):
        return Filter(lambda item: self._match(item) or other._match(item))


class Filter(BaseFilter[_T_co]):
    """
    Check all items in the iterable, and yield only matches.
    """

    def __init__(self, match, *args, **kwargs):
        self.__match = match
        self.__args = args
        self.__kwargs = kwargs

    def _match(self, item) -> bool:
        return self.__match(item, *self.__args, **self.__kwargs)


remove_empty = Filter(bool)
