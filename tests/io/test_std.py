from io import StringIO

from stream.io.std import StdIn


def test_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('abc\n123\n'))

    f = StdIn()
    assert tuple(f) == ('abc\n', '123\n')


def test_stdin_buffer(tmpdir, monkeypatch):
    file = tmpdir / '0.txt'
    file.write_text('abc\n123\n', encoding='utf-8')

    monkeypatch.setattr('sys.stdin', open(str(file)))

    f = StdIn()
    assert tuple(f.buffer) == (b'abc\n', b'123\n')
