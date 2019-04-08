from sqlalchemy.orm import (
    Query as _Query,
)

from stream import (
    Stream as _Stream,
    IterStream as _IterStream,
)
from . import (
    BaseDatabaseTable as _BaseDatabaseTable,
)


class DatabaseTableRead(_BaseDatabaseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__query = None

    def get_query(self, *fields) -> _Query:
        if len(fields) == 0:
            return self.session.query(self.model)
        else:
            return self.session.query(*fields)

    @property
    def query(self) -> _Query:
        if self.__query is None:
            self.__query = self.get_query()
        return self.__query

    @query.setter
    def query(self, val: _Query):
        self.__query = val

    @property
    def stream(self) -> _Stream:
        return _IterStream(self.query)
