from typing import Callable

from stream.functions.counting import (
    report as _report,
    log as _log,
)
from . import from_function

report = from_function(_report, has_params=True)


class log(object):
    __self = from_function(_log, has_params=True)

    """
    Log progress of a generator
    """

    def __init__(
            self,
            *,
            log_func: Callable[[str], None] = print,
            name=None,
            interval=1000,
    ):
        self.__log = log_func
        self.__name = name
        self.__interval = interval

    def __call__(self, gen):
        name = self.__name or gen.__name__
        return self.__self(
            log_func=self.__log,
            name=name,
            interval=self.__interval,
        )(gen)
