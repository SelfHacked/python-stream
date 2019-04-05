import sys as _sys
import typing as _typing

from gimme_cached_property import cached_property

from . import (
    TextFile as _TextFile,
    BinaryFile as _BinaryFile,
    _wrapper,
)


class StdIn(_wrapper.wrapper_class(_TextFile, lambda: _sys.stdin)):
    def __init__(self):
        # no param
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, StdIn)

    @cached_property
    def _buffer_class(self) -> _typing.Type[_BinaryFile]:
        class BufferClass(_wrapper.wrapper_class(_BinaryFile, lambda: _sys.stdin.buffer)):
            def __eq__(self, other):
                return isinstance(other, BufferClass)

        return BufferClass

    @cached_property
    def buffer(self) -> _BinaryFile:
        return self._buffer_class()
