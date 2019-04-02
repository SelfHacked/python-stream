import pytest

from stream.io import BinaryFile, TextFile


class DummyFile(BinaryFile):
    def __init__(self):
        self.__closed = False
        self.__iter = iter(b"""123
45

6
""")

    def close(self) -> None:
        self.__closed = True

    @property
    def closed(self) -> bool:
        return self.__closed

    def readable(self) -> bool:
        return True

    def _read_character(self) -> int:
        try:
            return next(self.__iter)
        except StopIteration:
            raise self.EOF


class DummyTextFile(TextFile):
    def __init__(self):
        self.__closed = False
        self.__iter = iter("""123
abc
""")

    def close(self) -> None:
        self.__closed = True

    @property
    def closed(self) -> bool:
        return self.__closed

    def readable(self) -> bool:
        return True

    def _read_character(self) -> str:
        try:
            return next(self.__iter)
        except StopIteration:
            raise self.EOF


def test_with():
    f = DummyFile()

    with f:
        assert not f.closed
    assert f.closed

    with pytest.raises(f.Closed):
        with f:
            pass


@pytest.mark.dependency(
    depends=['test_with'],
)
def test_read():
    with DummyFile() as f:
        assert f.read(0) == b''
        assert f.read(1) == b'1'
        assert f.read(3) == b'23\n'
        assert f.read() == b'45\n\n6\n'


@pytest.mark.dependency(
    depends=['test_with'],
)
def test_readline():
    with DummyFile() as f:
        assert f.readline(0) == b''
        assert f.readline(1) == b'1'
        assert f.readline() == b'23\n'
        assert f.readline(100) == b'45\n'


@pytest.mark.dependency(
    depends=['test_with'],
)
def test_readlines():
    with DummyFile() as f:
        assert f.readlines(0) == []
        assert f.readlines(1) == [b'123\n']
        assert f.readlines(2) == [b'45\n', b'\n']
        assert f.readlines() == [b'6\n']


@pytest.mark.dependency(
    depends=['test_with'],
)
def test_iter():
    with DummyFile() as f:
        assert next(f) == b'123\n'
        assert tuple(f) == (b'45\n', b'\n', b'6\n')


@pytest.mark.dependency(
    depends=['test_with'],
)
def test_stream():
    with DummyTextFile() as f:
        assert tuple(f.stream) == ('123\n', 'abc\n')
