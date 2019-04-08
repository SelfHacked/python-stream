import pytest

from stream.sql.read import DatabaseTableRead


def test_no_session(create_db):
    Model, engine = create_db

    table = DatabaseTableRead(Model, engine=engine)
    with pytest.raises(DatabaseTableRead.SessionStateError):
        table.session


def test_multiple_with(create_db):
    Model, engine = create_db

    with DatabaseTableRead(Model, engine=engine) as table:
        with pytest.raises(DatabaseTableRead.SessionStateError):
            with table:
                pass
