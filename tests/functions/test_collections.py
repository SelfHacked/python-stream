from stream.functions.collections import yield_from, GetItem


def test_yield_from():
    assert tuple(yield_from(('123', '456'))) == tuple('123456')


def test_getitem():
    get_1 = GetItem(1)
    assert tuple(get_1(('123', '45', 'abc'))) == ('2', '5', 'b')
