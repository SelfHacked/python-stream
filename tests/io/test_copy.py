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
def test_copy_local(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    file2 = tmpdir / '1.txt'
    with LocalFile(str(file)) as f1:
        with LocalFile(str(file2), 'w') as f2:
            f1.copy_to(f2)

    assert file2.read_text(encoding='utf-8') == txt


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/io/test_base.py::test_with'),
    ],
)
def test_same_file(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file)) as f1:
        with LocalFile(str(file), 'w') as f2:
            with pytest.raises(LocalFile.SameFile):
                f1.copy_to(f2)
