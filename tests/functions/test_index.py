import string

from logical.comparison import GreaterThan
from logical.num import is_odd

from stream.functions.index import ApplyAtIndex


def test_apply_at_index():
    assert ''.join(
        ApplyAtIndex(is_odd, str.upper)(string.ascii_lowercase)
    ) == 'aBcDeFgHiJkLmNoPqRsTuVwXyZ'


def test_index():
    assert ''.join(
        ApplyAtIndex(3, str.upper)(string.ascii_lowercase)
    ) == 'abcDefghijklmnopqrstuvwxyz'


def test_index_collection():
    assert ''.join(
        ApplyAtIndex(range(0, 26, 3), str.upper)(string.ascii_lowercase)
    ) == 'AbcDefGhiJklMnoPqrStuVwxYz'


def test_ended():
    assert ''.join(
        ApplyAtIndex(is_odd, str.upper, ended=GreaterThan(10))(string.ascii_lowercase)
    ) == 'aBcDeFgHiJkLmnopqrstuvwxyz'


def test_last_index():
    assert ''.join(
        ApplyAtIndex(is_odd, str.upper, ended=11)(string.ascii_lowercase)
    ) == 'aBcDeFgHiJkLmnopqrstuvwxyz'
