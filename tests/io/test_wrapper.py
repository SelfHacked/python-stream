from stream.io.local import LocalFile
from .util import depends_with

txt = """123
abc
"""


@depends_with()
def test_buffer_eq(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with LocalFile(str(file)) as f1:
        with f1.buffer as buffer:
            assert buffer == f1.buffer
            assert buffer != f1
            with LocalFile(str(file)) as f2:
                assert buffer == f2.buffer
            with LocalFile(str(tmpdir / '1.txt'), 'w') as f3:
                assert buffer != f3.buffer
