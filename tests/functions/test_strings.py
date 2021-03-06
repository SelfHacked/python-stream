from stream.functions.strings import strip, remove_comments, split_lines


def test_strip(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text("""123
abc
""", encoding='utf-8')

    with open(str(file)) as f:
        assert tuple(strip(f)) == ('123', 'abc')


def test_remove_comments():
    assert tuple(remove_comments(('#123', 'abc'))) == ('abc',)


def test_split_lines():
    assert tuple(split_lines((
        'abc\n\n123',
        '456\n',
        '789\n'
    ))) == (
               'abc\n',
               '\n',
               '123456\n',
               '789\n'
           )
