import sys as _sys

from . import (
    _wrapper,
)


class StdIn(_wrapper.text_wrapper_class(lambda: _sys.stdin)):
    def __init__(self):
        # no param
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, StdIn)
