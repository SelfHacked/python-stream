import typing as _typing

from stream.typing import (
    BaseParamFunction as _BaseParamFunction,
    T_co as _T_co,
    V_co as _V_co,
)


class BaseOneToOneFunction(_BaseParamFunction[_T_co, _V_co]):
    def _call(self, item):
        raise NotImplementedError  # pragma: no cover

    def __call__(self, iterable: _typing.Iterable[_T_co]) -> _typing.Iterator[_V_co]:
        for item in iterable:
            yield self._call(item)


class apply_each(BaseOneToOneFunction[_T_co, _V_co]):
    """
    Apply `func` to all items in the iterable.
    `func` must take each item as the first argument, and then take *args, **kwargs
    """

    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def _call(self, item):
        return self.__func(item, *self.__args, **self.__kwargs)
