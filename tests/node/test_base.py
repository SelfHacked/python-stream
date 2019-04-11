from typing import Iterator

import pytest

from stream import IterStream
from stream.node import Node, StreamStorage


class MergeNode(Node):
    """
    Merge streams into one.
    """

    def __merge(self) -> Iterator:
        for key in sorted(self.input):
            stream = self.input[key]
            for item in stream:
                yield key, item

    def _connect(self):
        self.output[None].store(self.__merge())


def test_merge():
    stream1 = IterStream(['abc', '123'])
    stream2 = IterStream(range(3))

    node = MergeNode()
    stream1 > node.input[0].store
    stream2 > node.input[1].store

    merged = tuple(node.output[None])
    assert merged == (
        (0, 'abc'),
        (0, '123'),
        (1, 0),
        (1, 1),
        (1, 2),
    )


class SplitNode(Node):
    """
    Split one stream into multiple.
    Will load into memory upon connect().
    """

    def __init__(self, n: int):
        super().__init__()
        self.__n = n

    def _connect(self):
        lists = [
            []
            for _ in range(self.__n)
        ]
        i = 0
        for item in self.input[None]:
            lists[i].append(item)
            i += 1
            if i == self.__n:
                i = 0
        for i, li in enumerate(lists):
            self.output[i].store(li)


class ErrorNode(Node):
    """
    Connect will raise an error on the first try,
    but succeed if forced again.
    """

    class Error(Exception):
        pass

    def __init__(self):
        super().__init__()
        self.__tried = False

    def _connect(self):
        if not self.__tried:
            self.__tried = True
            raise self.Error


def test_split():
    stream = IterStream(range(10))

    node = SplitNode(3)
    stream > node.input[None].store

    assert tuple(node.output[0]) == (0, 3, 6, 9)
    assert tuple(node.output[1]) == (1, 4, 7)
    assert tuple(node.output[2]) == (2, 5, 8)


def test_missing_input():
    node = SplitNode(3)

    with pytest.raises(SplitNode.ConnectionError) as captured:
        node.output
    assert isinstance(captured.value.inner, StreamStorage.Empty)


def test_used_input():
    node = MergeNode()

    IterStream([]) > node.input[0].store
    with pytest.raises(StreamStorage.Used):
        IterStream([]) > node.input[0].store


def test_error():
    node = ErrorNode()

    with pytest.raises(SplitNode.ConnectionError) as captured:
        node.output
    assert isinstance(captured.value.inner, ErrorNode.Error)

    # should not run _connect() again
    with pytest.raises(SplitNode.ConnectionError) as captured:
        node.output
    assert isinstance(captured.value.inner, ErrorNode.Error)

    node.connect(force_retry=True)
    node.output  # no raise
