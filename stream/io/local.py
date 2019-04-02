import os as _os

from gimme_cached_property import cached_property

from . import (
    File as _File,
)


class LocalFile(_File):
    def __init__(
            self,
            path: str,
            mode: str = 'r',
            *args,
            **kwargs,
    ):
        """
        See params for `open`
        """
        self.__path = path
        self.__file = open(path, mode=mode, *args, **kwargs)

    @cached_property
    def path(self) -> str:
        return _os.path.realpath(self.__path)

    def __eq__(self, other: _File):
        if not isinstance(other, LocalFile):
            return False
        if self.path != other.path:
            return False
        return True

    def __getattribute__(self, name: str):
        if name in ('__dict__', '__class__'):
            return object.__getattribute__(self, name)
        if name in self.__dict__:
            return object.__getattribute__(self, name)
        if name in self.__class__.__dict__:
            return object.__getattribute__(self, name)

        try:
            return getattr(self.__file, name)
        except AttributeError:
            return super().__getattribute__(name)
