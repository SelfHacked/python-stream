import pytest

from stream.functions.collections import yield_from, GetItem, GetItems, ToDict, SelectKeys


def test_yield_from():
    assert tuple(yield_from(('123', '456'))) == tuple('123456')


def test_get_item():
    get_1 = GetItem(1)
    assert tuple(get_1(('123', '45', 'abc'))) == ('2', '5', 'b')


def test_error():
    get_1 = GetItem(1)
    with pytest.raises(IndexError):
        next(get_1(['a']))

    get_a = GetItem('a')
    with pytest.raises(KeyError):
        next((get_a([{'b': 0}])))


def test_fill_none():
    get_1 = GetItem(1, none=True)
    assert next(get_1(['a'])) is None

    get_a = GetItem('a', none=True)
    assert next((get_a([{'b': 0}]))) is None


def test_get_items():
    get = GetItems(0, 2)
    assert tuple(get(('123', 'abc', 'xyz'))) == (
        ('1', '3'),
        ('a', 'c'),
        ('x', 'z'),
    )


def test_to_dict():
    to_dict = ToDict('x', 'y', 'z')
    assert tuple(to_dict(('123', 'abc'))) == (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': 'a', 'y': 'b', 'z': 'c'},
    )


def test_select_keys():
    select_keys = SelectKeys('x', 'z')
    dicts = (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': 'a', 'y': 'b', 'z': 'c'},
    )
    assert tuple(select_keys(dicts)) == (
        {'x': '1', 'z': '3'},
        {'x': 'a', 'z': 'c'},
    )
