import pytest

from stream.io.local import LocalFile

txt = """123
abc
"""


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/io/test_base.py::test_with'),
    ],
)
def test_read_file(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file)) as f:
        assert f.read() == txt


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/io/test_base.py::test_with'),
    ],
)
def test_write_file(tmpdir):
    file = tmpdir / '0.txt'

    with LocalFile(str(file), 'w') as f:
        f.write(txt)

    assert file.read_text(encoding='utf-8') == txt
