import typing as _typing

T_co = _typing.TypeVar('T_co', covariant=True)  # Any type covariant containers.
V_co = _typing.TypeVar('V_co', covariant=True)  # Any type covariant containers.

Function = _typing.Callable[[_typing.Iterable[T_co]], _typing.Iterator[V_co]]


class BaseParamFunction(Function[T_co, V_co]):
    def __call__(self, iterable: _typing.Iterable[T_co]) -> _typing.Iterator[V_co]:
        raise NotImplementedError  # pragma: no cover
