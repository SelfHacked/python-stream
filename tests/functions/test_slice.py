import string

from stream.functions.slice import Head, Since


def test_head():
    assert ''.join(
        Head(10)(string.ascii_lowercase)
    ) == 'abcdefghij'


def test_since():
    assert ''.join(
        Since(20)(string.ascii_lowercase)
    ) == 'uvwxyz'


def test_not():
    assert ''.join(
        (~Head(20))(string.ascii_lowercase)
    ) == 'uvwxyz'


def test_and():
    assert ''.join(
        (Since(10) & Head(20))(string.ascii_lowercase)
    ) == 'klmnopqrst'


def test_or():
    assert ''.join(
        (Head(10) | Since(20))(string.ascii_lowercase)
    ) == 'abcdefghijuvwxyz'
