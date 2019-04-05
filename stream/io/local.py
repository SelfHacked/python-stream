import os as _os

from gimme_cached_property import cached_property

from . import (
    File as _File,
    _wrapper,
)


class LocalFile(_wrapper.wrapper_class(_File, open)):
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
        super().__init__(path, mode, *args, **kwargs)
        self.__path = path

    @cached_property
    def path(self) -> str:
        return _os.path.realpath(self.__path)

    def __eq__(self, other: _File):
        if not isinstance(other, LocalFile):
            return False
        if self.path != other.path:
            return False
        return True
