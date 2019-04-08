from io import SEEK_CUR

import pytest

from stream.io.iterable import IterableFile
from .util import depends_with


def get() -> IterableFile:
    return IterableFile([b"""123
45

6
"""])


@depends_with()
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


@depends_with(
    ('session', 'tests/io/test_base.py::test_read'),
)
def test_tell():
    with get() as f:
        assert f.tell() == 0
        f.read(1)
        assert f.tell() == 1
        f.read(3)
        assert f.tell() == 4
        f.read()
        assert f.tell() == 10


@depends_with()
def test_seekable():
    with get() as f:
        assert f.seekable()
        with pytest.raises(OSError):
            f.truncate()


@depends_with()
def test_seek_forward_only():
    with get() as f:
        with pytest.raises(OSError):
            f.seek(0, 2)
        assert f.seek(2) == 2
        with pytest.raises(OSError):
            f.seek(0, 0)
        with pytest.raises(OSError):
            f.seek(-1, 1)


@depends_with(
    ('session', 'tests/io/test_base.py::test_read'),
    'test_tell',
)
def test_seek():
    with get() as f:
        f.seek(2)
        assert f.tell() == 2
        assert f.read(1) == b'3'
        f.seek(2, SEEK_CUR)
        assert f.tell() == 5
        assert f.read(1) == b'5'


@depends_with()
def test_os():
    with get() as f:
        assert f.mode == 'rb'
        assert not f.closed
        with pytest.raises(OSError):
            f.fileno()
        assert not f.isatty()
