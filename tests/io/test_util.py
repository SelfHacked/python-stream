from stream.io.util import characters

txt = """123
abc
"""


def test_characters_iter(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text(txt, encoding='utf-8')

    with open(str(file)) as f:
        characters_iter = characters(f)
        assert next(characters_iter) == '1'
        assert f.tell() == 1
        assert f.readline() == '23\n'
        assert f.tell() == 4
        assert next(characters_iter) == 'a'
        assert f.tell() == 5
        assert tuple(characters_iter) == ('b', 'c', '\n')
