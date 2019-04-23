import gzip

from stream.functions.bytes import un_gzip
from stream.io.local import LocalFile


def test_un_gzip(tmpdir):
    file = str(tmpdir / '0.txt.gz')
    with gzip.open(file, mode='wb') as f:
        f.write(b"""#123

456
""")

    assert tuple(
        LocalFile(file, mode='rb').stream
        | un_gzip
    ) == (
               b'#123\n',
               b'\n',
               b'456\n',
           )
