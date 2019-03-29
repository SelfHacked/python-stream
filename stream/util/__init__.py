import typing as _typing
from functools import (
    wraps as _wraps,
)


class returns(object):
    """
    Copied from selfhacked-util to minimize dependency.
    """

    def __init__(self, type_: _typing.Type):
        self.__type = type_

    def __call__(self, func):
        @_wraps(func)
        def __new_func(*args, **kwargs):
            return self.__type(func(*args, **kwargs))

        return __new_func
