from time import sleep

import pytest

from stream.functions.control import Preload
from stream.util.testing import assert_time


def dummy_iterable():
    sleep(0.1)
    yield 0


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/util/test_testing.py::test_assert_time'),
    ],
)
def test_preload_all():
    with assert_time(0.1):
        iterator = Preload(n=None)(dummy_iterable())
    with assert_time(0):
        assert tuple(iterator) == (0,)
