import typing as _typing

from gimme_cached_property import cached_property
from sqlalchemy.engine import (
    Engine as _Engine,
    create_engine as _create_engine,
)
from sqlalchemy.ext.declarative.api import (
    DeclarativeMeta as _DeclarativeMeta,
)
from sqlalchemy.orm import (
    Session as _Session,
    sessionmaker as _sessionmaker,
)

Model = _typing.TypeVar('Model', bound=_DeclarativeMeta)


class BaseDatabaseTable(object):
    def __init__(
            self,
            model: _typing.Type[Model],
            *,
            engine: _typing.Union[_Engine, str],
            session: _Session = None,
    ):
        self.__model = model

        if isinstance(engine, str):
            engine = _create_engine(engine)
        self.__engine = engine

        self.__session = session

    @property
    def model(self) -> _typing.Type[Model]:
        return self.__model

    @property
    def engine(self) -> _Engine:
        return self.__engine

    @property
    def session(self) -> _Session:
        if self.__session is None:
            self.__session = self._session_class()
        return self.__session

    @cached_property
    def _session_class(self) -> _sessionmaker:
        return _sessionmaker(bind=self.engine)
