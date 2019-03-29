import typing as _typing

from stream.typing import (
    Function as _Function,
)
from .each import (
    apply_each as _apply_each,
)
from .filter import (
    filter_ as _filter,
)

strip: _Function[str, str] = _apply_each(str.strip)

remove_comments: _filter[str] = ~_filter(str.startswith, '#')


def split_lines(iterable: _typing.Iterable[str]) -> _typing.Iterator[str]:
    """
    :param iterable: a series of strings, not necessarily split by lines
    :return: a series of strings split by lines

    E.g.
        ('123', '45\n6\n') | split_lines -> ('12345\n', '6\n')
    """
    remaining = ''
    for item in iterable:
        lines = (remaining + item).splitlines(keepends=True)
        remaining = lines.pop(-1)
        yield from lines
    if remaining:
        yield remaining
