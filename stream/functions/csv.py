import csv as _csv
import typing as _typing

from stream.functions.each import (
    BaseOneToOneFunction as _BaseOneToOneFunction,
)

CsvRow = _typing.List[str]


class Csv(_BaseOneToOneFunction[str, CsvRow]):
    def __init__(self, *args, **kwargs):
        """
        :param args: and
        :param kwargs:
            See csv.reader
        """
        self.__args = args
        self.__kwargs = kwargs

    def _call(self, item: str) -> CsvRow:
        return next(_csv.reader([item], *self.__args, **self.__kwargs))
