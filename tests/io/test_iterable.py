from io import SEEK_CUR

import pytest

from stream.io.iterable import IterableFile


def get() -> IterableFile:
    return IterableFile([b"""123
45

6
"""])


def test_readonly():
    with get() as f:
        assert f.readable()
        assert not f.writable()
        with pytest.raises(OSError):
            f.write(b'0')
        with pytest.raises(OSError):
            f.writelines([b'1', b'2'])
        with pytest.raises(OSError):
            f.flush()


def test_tell():
    with get() as f:
        assert f.tell() == 0
        f.read(1)
        assert f.tell() == 1
        f.read(3)
        assert f.tell() == 4
        f.read()
        assert f.tell() == 10


def test_seekable():
    with get() as f:
        assert f.seekable()
        with pytest.raises(OSError):
            f.truncate()


def test_seek_forward_only():
    with get() as f:
        with pytest.raises(OSError):
            f.seek(0, 2)
        assert f.seek(2) == 2
        with pytest.raises(OSError):
            f.seek(0, 0)
        with pytest.raises(OSError):
            f.seek(-1, 1)


def test_seek():
    with get() as f:
        f.seek(2)
        assert f.tell() == 2
        assert f.read(1) == b'3'
        f.seek(2, SEEK_CUR)
        assert f.tell() == 5
        assert f.read(1) == b'5'


def test_os():
    with get() as f:
        assert f.mode == 'rb'
        assert not f.closed
        with pytest.raises(OSError):
            f.fileno()
        assert not f.isatty()


def test_eq():
    with get() as f1, get() as f2:
        assert f1 != f2
