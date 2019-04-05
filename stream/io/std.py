import sys as _sys

from . import (
    TextFile as _TextFile,
    _wrapper,
)


class StdIn(_wrapper.text_wrapper_class(_TextFile, lambda: _sys.stdin)):
    def __init__(self):
        # no param
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, StdIn)
