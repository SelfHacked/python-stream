from logical.num import is_odd

from stream.functions.conditional import ApplyIf


def test_apply_if():
    assert tuple(ApplyIf(is_odd, str)(range(10))) == (
        0, '1', 2, '3', 4, '5', 6, '7', 8, '9',
    )
