import io as _io
import typing as _typing
from io import (
    BytesIO as _BytesIO,
)
from tempfile import (
    TemporaryFile as _TemporaryFile,
)

import boto3 as _boto3
from botocore.response import (
    StreamingBody as _StreamingBody,
)
from gimme_cached_property import cached_property

from stream.io import (
    BinaryFile as _BinaryFile,
)


class BaseS3File(_BinaryFile):
    s3 = _boto3.resource('s3')

    def __init__(
            self,
            bucket: str,
            key: str,
    ):
        """
        :param bucket: S3 bucket name.
        :param key: S3 file name.
        """
        self.__bucket = bucket
        self.__key = key

    @property
    def bucket(self) -> str:
        return self.__bucket

    @property
    def key(self) -> str:
        return self.__key

    @property
    def _obj(self):
        return self.s3.Object(self.__bucket, self.__key)

    def __eq__(self, other):
        if not isinstance(other, BaseS3File):
            return False
        if not self.bucket == other.bucket:
            return False
        if not self.key == other.key:
            return False
        return True

    # --- os ---

    @property
    def name(self) -> str:
        return f"s3://{self.bucket}/{self.key}"

    def fileno(self) -> int:
        raise self.NotSupported

    @property
    def isatty(self) -> bool:
        return False

    # --- seek ---

    def seekable(self) -> bool:
        return False

    def tell(self) -> int:
        raise self.NotSupported

    def seek(self, offset: int, whence: int = _io.SEEK_SET) -> int:
        raise self.NotSupported

    def truncate(self, size: _typing.Optional[int] = None) -> int:
        raise self.NotSupported


class S3ReadFile(BaseS3File):
    def __init__(
            self,
            bucket: str,
            key: str,
            *,
            lines: bool,
            chunk_size: int = 1024,
    ):
        """
        :param lines:
            Read the file by line vs by chunk.
            If False, readline(), readlines(), __next__() and __iter__()
            will return chunks instead of lines.
        :param chunk_size:
            Chunk size when reading from s3.
            Default is 1024.
        """
        super().__init__(bucket, key)

        self.__lines = lines
        self.__chunk_size = chunk_size

        self.__current_chunk = b''
        self.__closed = False

    @cached_property
    def __body(self) -> _StreamingBody:
        return self._obj.get()['Body']

    @cached_property
    def __chunks(self) -> _typing.Iterator[bytes]:
        if self.__lines:
            yield from self.__body.iter_lines(chunk_size=self.__chunk_size)
        else:
            yield from self.__body.iter_chunks(chunk_size=self.__chunk_size)

    # --- os ---

    @property
    def mode(self) -> str:
        return 'rb'

    def close(self) -> None:
        try:
            self.__body.close()
        finally:
            self.__closed = True

    @property
    def closed(self) -> bool:
        return self.__closed

    # --- read ---

    def readable(self) -> bool:
        return True

    def __load_current_chunk(self):
        if not self.__current_chunk:
            self.__current_chunk = next(self.__chunks)

    def _read_character(self) -> int:
        self.__load_current_chunk()
        try:
            return self.__current_chunk[0]
        finally:
            self.__current_chunk = self.__current_chunk[1:]

    def read(self, n: int = -1) -> bytes:
        if n == -1:
            return self.__body.read()
        return super().read(n=n)

    def readline(self, limit: int = -1) -> bytes:
        if self.__lines:
            return super().readline(limit=limit)

        self.__load_current_chunk()
        try:
            return self.__current_chunk
        finally:
            self.__current_chunk = b''

    # --- not writable ---

    def writable(self) -> bool:
        return False

    def write(self, s: bytes) -> None:
        raise self.NotSupported

    def flush(self) -> None:
        raise self.NotSupported


class S3WriteFile(BaseS3File):
    def __init__(
            self,
            bucket: str,
            key: str,
            *,
            tmpfile: bool = False,
            multipart: bool = False,
    ):
        """
        :param tmpfile: Store pending write data in a tmp file vs in memory.
        :param multipart:
            Use multipart.

            If False, all data will be uploaded upon flush() call,
            after which the file is no longer writable.

            If True (NOT IMPLEMENTED), each part is uploaded upon flush() call,
            and close() finishes the upload.

            flush() is always called by close().
        """
        super().__init__(bucket, key)

        self.__tmpfile = tmpfile
        if multipart:
            raise NotImplementedError

        self.__closed = False
        self.__pending: _typing.BinaryIO = None

    def _upload_obj(self, obj: _typing.BinaryIO):
        try:
            self._obj.upload_fileobj(obj)
        finally:
            self.close()

    def _check_direct_upload(self):
        if self.closed:
            raise self.Closed
        if self.__pending is not None:
            raise self.NotSupported

    def upload_from(self, filename: str):
        """
        Directly upload from a file.
        """
        self._check_direct_upload()
        try:
            self._obj.upload_file(filename)
        finally:
            self.close()

    def upload(self, file: _typing.BinaryIO):
        """
        Directly upload from a file-like object
        """
        self._check_direct_upload()
        self._upload_obj(file)

    # --- os ---

    @property
    def mode(self) -> str:
        return 'wb'

    def close(self) -> None:
        self.flush()

    @property
    def closed(self) -> bool:
        return self.__closed

    # --- write ---

    def writable(self) -> bool:
        return True

    def _create_storage(self) -> _typing.BinaryIO:
        if self.__tmpfile:
            return _TemporaryFile()
        else:
            return _BytesIO()

    def write(self, s: bytes) -> None:
        if self.closed:
            raise self.Closed

        if self.__pending is None:
            self.__pending = self._create_storage()
        self.__pending.write(s)

    def writelines(self, lines: _typing.Iterable[bytes]) -> None:
        if self.closed:
            raise self.Closed

        if self.__pending is None:
            self.__pending = self._create_storage()
        self.__pending.writelines(lines)

    def flush(self) -> None:
        try:
            self.__pending.seek(0, 0)
            self._upload_obj(self.__pending)
            self.__pending.close()
        finally:
            self.__closed = True

    # --- not readable ---

    def readable(self) -> bool:
        return False

    def _read_character(self) -> bytes:
        raise self.NotSupported


def upload_cmd():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('bucket')
    parser.add_argument('key')
    args = parser.parse_args()
    S3WriteFile(args.bucket, args.key).upload_from(args.file)


def download_cmd():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket')
    parser.add_argument('key')
    parser.add_argument('file')
    args = parser.parse_args()
    with open(args.file, 'wb') as f:
        for chunk in S3ReadFile(args.bucket, args.key, lines=False):
            f.write(chunk)


def get_cmd():
    """
    Stream to stdout
    """
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket')
    parser.add_argument('key')
    args = parser.parse_args()
    for chunk in S3ReadFile(args.bucket, args.key, lines=False):
        sys.stdout.buffer.write(chunk)


def copy_cmd():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('from_bucket', metavar='from-default')
    parser.add_argument('from_key', metavar='from-key')
    parser.add_argument('--to-bucket')
    parser.add_argument('--to-key')
    parser.add_argument('--tmpfile', action='store_true')
    args = parser.parse_args()

    S3ReadFile(
        args.from_bucket,
        args.from_key,
        lines=False,
    ).copy_to(S3WriteFile(
        args.to_bucket or args.from_bucket,
        args.to_key or args.from_key,
        tmpfile=args.tmpfile,
    ))
