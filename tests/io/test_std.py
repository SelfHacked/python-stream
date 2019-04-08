from io import StringIO

from stream.io.std import StdIn, StdOut, StdErr
from .util import depends_with


@depends_with()
def test_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('abc\n123\n'))

    with StdIn() as f:
        assert tuple(f) == ('abc\n', '123\n')


@depends_with()
def test_stdin_buffer(tmpdir, monkeypatch):
    file = tmpdir / '0.txt'
    file.write_text('abc\n123\n', encoding='utf-8')

    monkeypatch.setattr('sys.stdin', open(str(file)))

    with StdIn() as f:
        assert tuple(f.buffer) == (b'abc\n', b'123\n')


@depends_with()
def test_stdout_stderr(capsys):
    with StdOut() as f1:
        f1.write('hello')
    with StdErr() as f2:
        f2.write('world')
    captured = capsys.readouterr()
    assert captured.out == 'hello'
    assert captured.err == 'world'


def test_equal():
    assert StdIn() == StdIn()
    assert StdOut() == StdOut()
    assert StdErr() == StdErr()

    assert StdIn() != StdOut()
    assert StdOut() != StdErr()
    assert StdErr() != StdIn()

    assert StdIn().buffer == StdIn().buffer
    assert StdOut().buffer == StdOut().buffer
    assert StdErr().buffer == StdErr().buffer

    assert StdIn().buffer != StdOut().buffer
    assert StdOut().buffer != StdErr().buffer
    assert StdErr().buffer != StdIn().buffer
