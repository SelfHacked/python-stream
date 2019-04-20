from logical.num import is_odd

from stream.functions.logging import LogIf


def test_log_if():
    logs = []
    log = LogIf(is_odd, logs.append, str)
    assert tuple(log(range(10))) == tuple(range(10))
    assert logs == ['1', '3', '5', '7', '9']
