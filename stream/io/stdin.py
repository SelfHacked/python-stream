from stream import (
    Stream as _Stream,
)


class InputStream(_Stream[str]):
    def __next__(self) -> str:
        try:
            return input()
        except EOFError:
            raise StopIteration
