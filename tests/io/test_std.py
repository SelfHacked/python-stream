from io import StringIO

import pytest

from stream.io.std import StdIn


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/io/test_base.py::test_with'),
    ],
)
def test_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('abc\n123\n'))

    with StdIn() as f:
        assert tuple(f) == ('abc\n', '123\n')


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/io/test_base.py::test_with'),
    ],
)
def test_stdin_buffer(tmpdir, monkeypatch):
    file = tmpdir / '0.txt'
    file.write_text('abc\n123\n', encoding='utf-8')

    monkeypatch.setattr('sys.stdin', open(str(file)))

    with StdIn() as f:
        assert tuple(f.buffer) == (b'abc\n', b'123\n')
