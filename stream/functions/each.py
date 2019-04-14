import typing as _typing

from stream.typing import (
    Function as _Function,
    T_co as _T_co,
    V_co as _V_co,
)


class BaseOneToOneFunction(_Function[_T_co, _V_co]):
    def each(self, item: _T_co) -> _V_co:
        raise NotImplementedError  # pragma: no cover

    def __call__(self, iterable: _typing.Iterable[_T_co]) -> _typing.Iterator[_V_co]:
        for item in iterable:
            yield self.each(item)


class ApplyEach(BaseOneToOneFunction[_T_co, _V_co]):
    """
    Apply `func` to all items in the iterable.
    `func` must take each item as the first argument, and then take *args, **kwargs
    """

    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def each(self, item: _T_co) -> _V_co:
        return self.__func(item, *self.__args, **self.__kwargs)
