import pytest

from stream.decorators.control import preload


def test_partial():
    @preload()
    def gen(out_list):
        out_list.append(0)
        yield 1
        out_list.append(2)

    results = []
    generator = gen(results)
    assert results == [0]
    assert list(generator) == [1]
    assert results == [0, 2]


def test_empty():
    @preload()
    def gen():
        yield from ()

    assert tuple(gen()) == ()

    @preload(not_enough_error=True)
    def gen2():
        yield from ()

    with pytest.raises(StopIteration):
        gen2()

    @preload(not_enough_error=ValueError)
    def gen3():
        yield from ()

    with pytest.raises(ValueError):
        gen3()
