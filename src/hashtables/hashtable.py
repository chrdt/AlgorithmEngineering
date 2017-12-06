from __future__ import print_function
import abc
from collections import namedtuple


class HashTable(object):
    __metaclass__ = abc.ABCMeta
    entry = namedtuple("entry", ["key", "value"])
    bottom = entry(None, None)

    @abc.abstractmethod
    def insert(self, key, value):
        # type: (int ,int) -> None
        pass

    @abc.abstractmethod
    def delete(self, key):
        # type: (int) -> None
        pass

    @abc.abstractmethod
    def search(self, key):
        # type: (int) -> int
        pass

    @abc.abstractmethod
    def pprint(self):
        # type: () -> None
        pass

    @abc.abstractmethod
    def tosequence(self):
        # type: () -> str
        pass
