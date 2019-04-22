import typing as _typing

from logical import (
    BaseFunction as _BaseLogicalFunction,
    Function as _LogicalFunction,
)
from logical.boolean import (
    false as _false,
)
from logical.collection import (
    In as _In,
)
from logical.comparison import (
    Equal as _Equal,
    GreaterThanOrEqual as _Ge,
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

    @property
    def ended_f(self) -> _BaseLogicalFunction:
        raise NotImplementedError  # pragma: no cover

    def match_index(self, index: int) -> bool:
        raise NotImplementedError  # pragma: no cover

    def ended(self, index: int) -> bool:
        raise NotImplementedError  # pragma: no cover


class MatchIndexFunc(BaseMatchIndexFunc):
    def __init__(self, match: Index):
        if isinstance(match, int):
            ended = _Ge(match)
            match = _Equal(match)
        elif isinstance(match, _typing.Collection):
            ended = _Ge(max(match))
            match = _In(match)
        else:
            ended = _false
        self.__match = _LogicalFunction.get(match)
        self.__ended = ended

    @property
    def match_index_f(self) -> _BaseLogicalFunction:
        return self.__match

    @property
    def ended_f(self) -> _BaseLogicalFunction:
        return self.__ended

    def match_index(self, index: int) -> bool:
        return self.match_index_f(index)

    def ended(self, index: int) -> bool:
        return self.ended_f(index)
