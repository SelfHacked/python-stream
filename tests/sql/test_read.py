from stream.sql.read import DatabaseTableRead


def test_read(populate_db):
    Model, engine = populate_db

    with DatabaseTableRead(Model, engine=engine) as table:
        assert {
                   item.key: item.value
                   for item in table.stream
               } == {
                   1: 'x',
                   2: 'y',
                   3: 'y',
               }


def test_filter(populate_db):
    Model, engine = populate_db

    with DatabaseTableRead(Model, engine=engine) as table:
        table.query = table.get_query().filter_by(value='y')

        assert {
                   item.key: item.value
                   for item in table.stream
               } == {
                   2: 'y',
                   3: 'y',
               }


def test_order_by(populate_db):
    Model, engine = populate_db

    with DatabaseTableRead(Model, engine=engine) as table:
        assert [
                   item.key
                   for item in table.stream
               ] == [1, 2, 3]

        table.query = table.get_query().order_by(-Model.key)
        assert [
                   item.key
                   for item in table.stream
               ] == [3, 2, 1]


def test_select_fields(populate_db):
    Model, engine = populate_db

    with DatabaseTableRead(Model, engine=engine) as table:
        table.query = table.get_query(Model.key, Model.value)
        assert tuple(table.stream) == (
            (1, 'x'),
            (2, 'y'),
            (3, 'y'),
        )
