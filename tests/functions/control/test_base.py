from time import sleep

from stream.functions.control import preload_all
from stream.util.testing import assert_time


def get_items():
    sleep(0.1)
    yield 0


def test_preload_all():
    with assert_time(0.1):
        iterator = preload_all(get_items())
    with assert_time(0):
        assert tuple(iterator) == (0,)
