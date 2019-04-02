from stream.io.local import LocalFile


def test_file_stream(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text("""123
abc
""", encoding='utf-8')
    s = LocalFile(str(file)).stream
    assert tuple(s) == ('123\n', 'abc\n')
