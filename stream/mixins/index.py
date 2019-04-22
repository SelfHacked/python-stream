import typing as _typing

from logical import (
    BaseFunction as _BaseLogicalFunction,
    Function as _LogicalFunction,
)
from logical.collection import (
    In as _In,
)
from logical.comparison import (
    Equal as _Equal,
)

MatchIndex = _typing.Callable[[int], bool]
Index = _typing.Union[
    int,
    _typing.Collection[int],
    MatchIndex,
]


class BaseMatchIndexFunc(object):
    @property
    def match_index_f(self) -> _BaseLogicalFunction:
        raise NotImplementedError  # pragma: no cover

    def match_index(self, index: int) -> bool:
        raise NotImplementedError  # pragma: no cover


class MatchIndexFunc(BaseMatchIndexFunc):
    def __init__(self, match: Index):
        if isinstance(match, int):
            match = _Equal(match)
        elif isinstance(match, _typing.Collection):
            match = _In(match)
        self.__match = _LogicalFunction.get(match)

    @property
    def match_index_f(self) -> _BaseLogicalFunction:
        return self.__match

    def match_index(self, index: int) -> bool:
        return self.match_index_f(index)
