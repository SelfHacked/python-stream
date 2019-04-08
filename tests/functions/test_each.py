from stream.functions.each import ApplyEach


def test_apply_each():
    assert tuple(ApplyEach(str)((1, 2, 3))) == ('1', '2', '3')
