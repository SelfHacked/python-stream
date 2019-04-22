import typing as _typing

from stream.mixins.each import (
    Each as _Each,
    ItemFunc as _ItemFunc,
)
from stream.mixins.index import (
    Index as _Index,
    BaseMatchIndexFunc as _BaseMatchIndexFunc,
    MatchIndexFunc as _MatchIndexFunc,
)
from stream.typing import (
    T_co as _T_co,
    V_co as _V_co,
)
from .each import (
    BaseOneToOneFunction as _BaseOneToOneFunction,
)


class BaseApplyAtIndex(
    _BaseOneToOneFunction[_T_co, _V_co],
    _BaseMatchIndexFunc,
):
    def __call__(
            self,
            iterable: _typing.Iterable[_T_co],
    ) -> _typing.Iterator[_typing.Union[_T_co, _V_co]]:
        index = 0
        iterator = iter(iterable)
        for item in iterator:
            if self.match_index(index):
                yield self.each(item)
            else:
                yield item
            if self.ended(index):
                break
            index += 1
        yield from iterator


class ApplyAtIndex(
    BaseApplyAtIndex[_T_co, _V_co],
    _MatchIndexFunc,
    _ItemFunc,
):
    def __init__(
            self,
            match: _Index,
            each: _Each,
    ):
        _MatchIndexFunc.__init__(self, match)
        _ItemFunc.__init__(self, each)
