from stream.io.local import LocalFile

from .util import depends_with

txt = """123
abc
"""


@depends_with()
def test_read_file(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file)) as f:
        assert f.read() == txt


@depends_with()
def test_write_file(tmpdir):
    file = tmpdir / '0.txt'

    with LocalFile(str(file), 'w') as f:
        f.write(txt)

    assert file.read_text(encoding='utf-8') == txt
