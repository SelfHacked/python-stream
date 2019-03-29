from stream import IterStream


def test_iter_stream():
    s = IterStream('abc')
    assert tuple(s) == ('a', 'b', 'c')
