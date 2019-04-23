import pytest

from stream.io.local import LocalFile

txt = """123
abc
"""
bin = b"""123
abc
"""


def test_read_file(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file)) as f:
        assert f.read() == txt


def test_write_file(tmpdir):
    file = tmpdir / '0.txt'

    with LocalFile(str(file), 'w') as f:
        f.write(txt)

    assert file.read_text(encoding='utf-8') == txt


def test_read_buffer(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file)) as f:
        assert f.buffer.read() == bin


def test_write_buffer(tmpdir):
    file = tmpdir / '0.txt'

    with LocalFile(str(file), 'w') as f:
        f.buffer.write(bin)

    assert file.read_text(encoding='utf-8') == txt


def test_no_buffer(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file), 'rb') as f1:
        with pytest.raises(AttributeError):
            f1.buffer

    with LocalFile(str(file), 'wb') as f2:
        with pytest.raises(AttributeError):
            f2.buffer


def test_next(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file)) as f:
        assert next(f) == '123\n'
