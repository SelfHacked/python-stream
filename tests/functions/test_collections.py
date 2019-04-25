import pytest

from stream.functions.collections import yield_from, GetItem, GetItems, ToDict, SelectKeys, ApplyOnKeys, ReplaceKeys


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


def test_apply_on_keys():
    apply = ApplyOnKeys(int, 'x')
    dicts = (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': '10', 'y': 'b', 'z': 'c'},
    )
    assert tuple(apply(dicts)) == (
        {'x': 1, 'y': '2', 'z': '3'},
        {'x': 10, 'y': 'b', 'z': 'c'},
    )
    assert dicts == (
        {'x': 1, 'y': '2', 'z': '3'},
        {'x': 10, 'y': 'b', 'z': 'c'},
    )


def test_apply_on_all():
    apply = ApplyOnKeys(int)
    dicts = (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': '10', 'y': '20', 'z': '30'},
    )
    assert tuple(apply(dicts)) == (
        {'x': 1, 'y': 2, 'z': 3},
        {'x': 10, 'y': 20, 'z': 30},
    )
    assert dicts == (
        {'x': 1, 'y': 2, 'z': 3},
        {'x': 10, 'y': 20, 'z': 30},
    )


def test_copy():
    apply = ApplyOnKeys(int, copy=True)
    dicts = (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': '10', 'y': '20', 'z': '30'},
    )
    assert tuple(apply(dicts)) == (
        {'x': 1, 'y': 2, 'z': 3},
        {'x': 10, 'y': 20, 'z': 30},
    )
    assert dicts == (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': '10', 'y': '20', 'z': '30'},
    )


def test_apply_on_error():
    apply = ApplyOnKeys(int, 'x')
    dicts = (
        {'y': '2', 'z': '3'},
        {'x': 'a', 'y': 'b', 'z': 'c'},
    )
    with pytest.raises(KeyError):
        tuple(apply([dicts[0]]))
    with pytest.raises(ValueError):
        tuple(apply([dicts[1]]))


def test_apply_on_none():
    apply = ApplyOnKeys(int, 'x', none=True)
    dicts = (
        {'y': '2', 'z': '3'},
        {'x': 'a', 'y': 'b', 'z': 'c'},
    )
    assert tuple(apply(dicts)) == (
        {'x': None, 'y': '2', 'z': '3'},
        {'x': None, 'y': 'b', 'z': 'c'},
    )


def test_replace_keys():
    replace = ReplaceKeys({'x': 'a'})
    dicts = (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': '10', 'y': 'b', 'z': 'c'},
    )
    assert tuple(replace(dicts)) == (
        {'a': '1', 'y': '2', 'z': '3'},
        {'a': '10', 'y': 'b', 'z': 'c'},
    )
    assert dicts == (
        {'a': '1', 'y': '2', 'z': '3'},
        {'a': '10', 'y': 'b', 'z': 'c'},
    )


def test_replace_keys_copy():
    replace = ReplaceKeys({'x': 'a'}, copy=True)
    dicts = (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': '10', 'y': 'b', 'z': 'c'},
    )
    assert tuple(replace(dicts)) == (
        {'a': '1', 'y': '2', 'z': '3'},
        {'a': '10', 'y': 'b', 'z': 'c'},
    )
    assert dicts == (
        {'x': '1', 'y': '2', 'z': '3'},
        {'x': '10', 'y': 'b', 'z': 'c'},
    )


def test_replace_keys_error():
    replace = ReplaceKeys({'x': 'a'})
    dicts = (
        {'y': '2', 'z': '3'},
        {'x': 'a', 'y': 'b', 'z': 'c'},
    )
    with pytest.raises(KeyError):
        tuple(replace(dicts))


def test_replace_keys_none():
    replace = ReplaceKeys({'x': 'a'}, none=True)
    dicts = (
        {'y': '2', 'z': '3'},
        {'x': 'a', 'y': 'b', 'z': 'c'},
    )
    assert tuple(replace(dicts)) == (
        {'a': None, 'y': '2', 'z': '3'},
        {'a': 'a', 'y': 'b', 'z': 'c'},
    )
