import pytest

from stream import Stream, IterStream
from stream.functions.each import ApplyEach
from stream.functions.filter import remove_empty
from stream.functions.strings import strip, remove_comments


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/test_base.py::test_iter_stream'),
    ],
)
def test_or():
    s1 = IterStream('123')
    s2 = s1 | strip
    assert isinstance(s2, Stream)


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/test_base.py::test_iter_stream'),
    ],
)
def test_gt():
    s1 = IterStream('123')
    tu = s1 > tuple
    assert tu == ('1', '2', '3')


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/test_base.py::test_iter_stream'),
        'test_or',
        ('session', 'tests/functions/test_each.py::test_apply_each'),
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
        ('session', 'tests/test_base.py::test_iter_stream'),
        'test_or',
        ('session', 'tests/functions/test_strings.py::test_strip'),
        ('session', 'tests/functions/test_filter.py::test_remove_empty'),
        ('session', 'tests/functions/test_strings.py::test_remove_comments'),
    ],
)
def test_chain(tmpdir):
    assert tuple(
        IterStream("""#123

abc
""".splitlines(keepends=True))
        | strip
        | remove_empty
        | remove_comments
    ) == ('abc',)
