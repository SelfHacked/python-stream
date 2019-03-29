from typing import Callable, Iterable, Iterator

from stream.typing import T_co
from .each import BaseOneToOneFunction


class BaseReport(BaseOneToOneFunction[T_co, T_co]):
    def __init__(self, *, interval=1000):
        self.__interval = interval
        self.__count = 0

    def _interval_callback(self, n: int):
        raise NotImplementedError  # pragma: no cover

    def _finish_callback(self, n: int):
        raise NotImplementedError  # pragma: no cover

    def _call(self, item):
        self.__count += 1
        if self.__count % self.__interval == 0:
            self._interval_callback(self.__count)
        return item

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[T_co]:
        yield from super().__call__(iterable)
        self._finish_callback(self.__count)


class report(BaseReport[T_co]):
    """
    Report progress of an iterable
    """

    @staticmethod
    def none(n: int):
        pass  # pragma: no cover

    def __init__(
            self,
            *,
            interval=1000,
            interval_callback: Callable[[int], None] = None,
            finish_callback: Callable[[int], None] = None,
    ):
        super().__init__(interval=interval)
        self.__interval_callback = interval_callback or self.none
        self.__finish_callback = finish_callback or self.none

    def _interval_callback(self, n: int):
        self.__interval_callback(n)

    def _finish_callback(self, n: int):
        self.__finish_callback(n)


class log(BaseReport[T_co]):
    """
    Log progress of an iterable
    """

    def __init__(
            self,
            *,
            log_func: Callable[[str], None] = print,
            name,
            interval=1000,
    ):
        super().__init__(interval=interval)
        self.__name = name
        self.__log = log_func

    def _interval_callback(self, n: int):
        self.__log(f"{self.__name}: yielded {n} entries")

    def _finish_callback(self, n: int):
        self.__log(f"{self.__name}: finished with {n} entries")
