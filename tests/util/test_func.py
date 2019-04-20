import logging

from stream.util.func.logging import LoggerLog
from stream.util.func.partial import PartialFunc


def test_partial():
    startswith_hash = PartialFunc.get(str.startswith, '#')
    assert startswith_hash('#123')
    assert not startswith_hash('123')


def test_partial_get():
    def f(item, *args, **kwargs): pass

    assert PartialFunc.get(f) is f
    assert isinstance(PartialFunc.get(f, 0, x=1), PartialFunc)


def test_logger(caplog):
    caplog.set_level(0)
    info = LoggerLog('my_logger', level=logging.INFO)
    info('xyz')
    warning = LoggerLog('my_logger', level=logging.WARNING)
    warning('abc')
    assert caplog.record_tuples == [
        ('my_logger', logging.INFO, 'xyz'),
        ('my_logger', logging.WARNING, 'abc'),
    ]
