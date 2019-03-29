import gzip
from typing import Iterable, Iterator

from stream.typing import Function
from stream.util.io import BytesIterableAsIO
from .each import apply_each

decode: Function[bytes, str] = apply_each(bytes.decode, encoding='utf-8')


def un_gzip(iterable: Iterable[bytes]) -> Iterator[str]:
    """
    Unzip a gzip byte stream into str, and split by lines.
    """
    readable = BytesIterableAsIO(iterable)
    with gzip.open(readable) as f:
        yield from f
