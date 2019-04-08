from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stream import IterStream
from stream.sql.read import DatabaseTableRead
from stream.sql.write import DatabaseTableWrite


def test_write(create_db):
    Model, engine = create_db

    with DatabaseTableWrite(Model, engine=engine) as table:
        table.bulk_insert([
            Model(key=1, value='a'),
            Model(key=2, value='b'),
        ])

    # use new engine and session to validate
    engine2 = create_engine(engine.url)
    session = sessionmaker(bind=engine2)()
    assert {
               item.key: item.value
               for item in session.query(Model)
           } == {
               1: 'a',
               2: 'b',
           }


def test_truncate(populate_db):
    Model, engine = populate_db

    with DatabaseTableWrite(Model, engine=engine) as table:
        table.truncate()
        table.bulk_insert([
            Model(key=1, value='a'),
            Model(key=2, value='b'),
        ])

    # use new engine and session to validate
    engine2 = create_engine(engine.url)
    session = sessionmaker(bind=engine2)()
    assert {
               item.key: item.value
               for item in session.query(Model)
           } == {
               1: 'a',
               2: 'b',
           }


def test_stream(create_db):
    Model, engine = create_db

    stream = IterStream([
        Model(key=1, value='a'),
        Model(key=2, value='b'),
    ])
    with DatabaseTableWrite(Model, engine=engine) as table:
        stream > table.bulk_insert

    # use new engine and session to validate
    with DatabaseTableRead(Model, engine=engine.url) as table:
        assert {
                   item.key: item.value
                   for item in table.stream
               } == {
                   1: 'a',
                   2: 'b',
               }
