from functools import wraps
from typing import Type


class returns(object):
    """
    Copied from selfhacked-util to minimize dependency.
    """

    def __init__(self, type_: Type):
        self.__type = type_

    def __call__(self, func):
        @wraps(func)
        def __new_func(*args, **kwargs):
            return self.__type(func(*args, **kwargs))

        return __new_func
