from stream.functions.csv import Csv, ToDict


def test_csv():
    reader = Csv()
    assert tuple(reader(['x,y', '1,2'])) == (
        ['x', 'y'],
        ['1', '2'],
    )


def test_delimiter():
    reader = Csv(delimiter='\t')
    assert tuple(reader(['x\ty', '1\t2'])) == (
        ['x', 'y'],
        ['1', '2'],
    )


def test_to_dict():
    to_dict = ToDict()
    lines = (
        ['x', 'y'],
        ['1', '2'],
        ['3', '4'],
    )
    assert tuple(to_dict(lines)) == (
        {'x': '1', 'y': '2'},
        {'x': '3', 'y': '4'},
    )
