import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def create_db(tmpdir):
    Base = declarative_base()

    class Model(Base):
        __tablename__ = 'table'
        key = Column(Integer, primary_key=True)
        value = Column(String)

    db = tmpdir / 'db.sqlite'
    engine = create_engine(f"sqlite:///{db}")

    Base.metadata.create_all(engine)

    return Model, engine


@pytest.fixture
def populate_db(create_db):
    Model, engine = create_db

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all([
        Model(key=1, value='x'),
        Model(key=2, value='y'),
        Model(key=3, value='y'),
    ])
    session.commit()
    session.close()

    return Model, engine
