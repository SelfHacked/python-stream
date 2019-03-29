from stream.decorators.counting import log, report


def test_report():
    logs = []

    @report(interval=2, interval_callback=logs.append, finish_callback=logs.append)
    def gen():
        yield from range(10)

    generator = gen()
    assert next(generator) == 0
    assert logs == []

    assert next(generator) == 1
    assert logs == [2]

    assert list(generator) == [2, 3, 4, 5, 6, 7, 8, 9]
    assert logs == [2, 4, 6, 8, 10, 10]


def test_log():
    logs = []

    @log(log_func=logs.append, interval=2)
    def gen():
        yield from range(3)

    assert list(gen()) == [0, 1, 2]
    assert logs == [
        'gen: yielded 2 entries',
        'gen: finished with 3 entries',
    ]
