import typing as _typing

from . import (
    BaseDatabaseTable as _BaseDatabaseTable,
    Model as _Model,
)


class DatabaseTableWrite(_BaseDatabaseTable[_Model]):
    """
    Write access to a database table.
    """

    def __init__(
            self,
            *args,
            truncate: bool = False,
            **kwargs,
    ):
        """
        :param truncate: Truncate table before writing

        :param args: and
        :param kwargs:
            See base class
        """
        super().__init__(*args, **kwargs)
        self.__truncate = truncate

    @property
    def _truncate(self) -> bool:
        return self.__truncate

    def _truncate_table(self):
        try:
            self.engine.execute(f"TRUNCATE TABLE {self.model.__table__}")
        except Exception:
            self.get_query().delete()

    def bulk_insert(self, objects: _typing.Iterable[_Model]):
        if self._truncate:
            self._truncate_table()
        self.session.add_all(objects)
