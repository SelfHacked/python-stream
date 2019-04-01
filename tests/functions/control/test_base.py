from time import sleep

from stream.functions.control import preload
from stream.util.testing import assert_time


def dummy_iterable():
    sleep(0.1)
    yield 0


def test_preload_all():
    with assert_time(0.1):
        iterator = preload(n=None)(dummy_iterable())
    with assert_time(0):
        assert tuple(iterator) == (0,)
