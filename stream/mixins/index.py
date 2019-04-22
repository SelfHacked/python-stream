import typing as _typing

from logical import (
    BaseFunction as _BaseLogicalFunction,
    Function as _LogicalFunction,
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
    @staticmethod
    def index(i) -> MatchIndex:
        def match(x):
            return x == i

        return match

    @staticmethod
    def indexes(collection) -> MatchIndex:
        def match(x):
            return x in collection

        return match

    def __init__(self, match: Index):
        if isinstance(match, int):
            match = self.index(match)
        elif isinstance(match, _typing.Collection):
            match = self.indexes(match)
        self.__match = _LogicalFunction.get(match)

    @property
    def match_index_f(self) -> _BaseLogicalFunction:
        return self.__match

    def match_index(self, index: int) -> bool:
        return self.match_index_f(index)
