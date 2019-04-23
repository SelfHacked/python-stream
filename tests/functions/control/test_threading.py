from time import sleep

import pytest

from stream.functions.control.threading import Prefetch
from stream.util.testing import assert_time


def dummy_iterable():
    sleep(0.1)
    yield 0
    sleep(0.1)
    yield 1


def _test_prefetch(prefetch):
    iterator = prefetch(dummy_iterable())

    with assert_time(0.1):
        assert next(iterator) == 0

    sleep(0.1)
    # the second record should have been prefetched by now
    with assert_time(0):
        assert next(iterator) == 1

    with pytest.raises(StopIteration):
        next(iterator)


def test_prefetch_one():
    _test_prefetch(Prefetch())


def test_prefetch_all():
    _test_prefetch(Prefetch(n=None))


def test_timeout():
    iterator = Prefetch(n=None, timeout=1)(dummy_iterable())
    tuple(iterator)

    iterator = Prefetch(n=None, timeout=0)(dummy_iterable())
    with pytest.raises(Prefetch.Timeout):
        next(iterator)
