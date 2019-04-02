from stream.io.stdin import InputStream


def test_input_stream(monkeypatch):
    x = iter(['abc', '123'])

    def input():
        try:
            return next(x)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr('builtins.input', input)
    s = InputStream()
    assert tuple(s) == ('abc', '123')
