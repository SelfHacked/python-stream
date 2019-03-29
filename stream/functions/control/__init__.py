from typing import Union, Type, Iterable, Iterator

from stream.typing import BaseParamFunction, T_co


class preload(BaseParamFunction[T_co, T_co]):
    def __init__(
            self,
            *,
            n: int = 1,
            not_enough_error: Union[bool, Type[Exception]] = False,
    ):
        """
        :param n: Number of entries to preload.
        :param not_enough_error:
            If False (default), simply yield all entries;
            If True, raise StopIteration;
            Otherwise, raise not_enough_error().
        """
        self.__n = n
        self.__error = not_enough_error

    def __call__(self, iterable: Iterable[T_co]) -> Iterator[T_co]:
        iterator = iter(iterable)
        preloaded = []

        while len(preloaded) < self.__n:
            try:
                preloaded.append(next(iterator))
            except StopIteration:
                if not self.__error:
                    return iter(preloaded)
                elif self.__error is True:
                    raise
                else:
                    raise self.__error() from None

        def __generator():
            yield from preloaded
            yield from iterator

        return __generator()


def preload_all(iterable: Iterable[T_co]) -> Iterator[T_co]:
    preloaded = tuple(iterable)
    return iter(preloaded)
