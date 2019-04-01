import pytest

from stream import Stream, IterStream
from stream.functions.each import ApplyEach
from stream.functions.filter import remove_empty
from stream.functions.strings import strip, remove_comments
from stream.io import FileStream


def test_or():
    s1 = IterStream('123')
    s2 = s1 | strip
    assert isinstance(s2, Stream)


def test_gt():
    s1 = IterStream('123')
    tu = s1 > tuple
    assert tu == ('1', '2', '3')


@pytest.mark.dependency(
    depends=[
        'test_or',
    ],
)
def test_call():
    s = IterStream('abc')
    li = []
    s2 = s | ApplyEach(li.append)
    s2()
    assert li == ['a', 'b', 'c']


@pytest.mark.dependency(
    depends=[
        'test_or',
        ('session', 'tests/test_io.py::test_file_stream'),
        ('session', 'tests/functions/test_strings.py::test_strip'),
        ('session', 'tests/functions/test_filter.py::test_remove_empty'),
        ('session', 'tests/functions/test_strings.py::test_remove_comments'),
    ],
)
def test_chain(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text("""#123

abc
""", encoding='utf-8')

    assert tuple(
        FileStream(str(file))
        | strip
        | remove_empty
        | remove_comments
    ) == ('abc',)
