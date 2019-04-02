from . import (
    File as _File,
)


class LocalFile(_File):
    def __init__(self, *args, **kwargs):
        self.__file = open(*args, **kwargs)

    def __getattribute__(self, name: str):
        if name == '_LocalFile__file':
            return super().__getattribute__(name)
        try:
            return getattr(self.__file, name)
        except AttributeError:
            return super().__getattribute__(name)
