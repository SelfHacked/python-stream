from stream import Stream, IterStream
from stream.functions.each import ApplyEach
from stream.functions.filter import remove_empty
from stream.functions.strings import strip, remove_comments


def test_or():
    s1 = IterStream('123')
    s2 = s1 | strip
    assert isinstance(s2, Stream)


def test_gt():
    s1 = IterStream('123')
    tu = s1 > tuple
    assert tu == ('1', '2', '3')


def test_call():
    s = IterStream('abc')
    li = []
    s2 = s | ApplyEach(li.append)
    s2()
    assert li == ['a', 'b', 'c']


def test_chain(tmpdir):
    assert tuple(
        IterStream("""#123

abc
""".splitlines(keepends=True))
        | strip
        | remove_empty
        | remove_comments
    ) == ('abc',)
