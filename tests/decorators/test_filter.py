from stream.decorators.filter import remove_empty


def test_remove_empty():
    @remove_empty
    def gen():
        yield 1
        yield 0
        yield 2

    assert tuple(gen()) == (1, 2)
