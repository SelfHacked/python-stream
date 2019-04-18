from stream.util.func.partial import PartialFunc


def test_partial():
    startswith_hash = PartialFunc.get(str.startswith, '#')
    assert startswith_hash('#123')
    assert not startswith_hash('123')


def test_partial_get():
    def f(item, *args, **kwargs): pass

    assert PartialFunc.get(f) is f
    assert isinstance(PartialFunc.get(f, 0, x=1), PartialFunc)

