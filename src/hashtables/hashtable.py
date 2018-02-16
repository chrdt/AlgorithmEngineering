import abc
from collections import namedtuple


class HashTable(object):
    __metaclass__ = abc.ABCMeta
    entry = namedtuple("entry", ["key", "value"])
    bottom = entry(None, None)

    class InsertionException(Exception):
        pass

    @abc.abstractmethod
    def insert(self, key, value):
        pass

    @abc.abstractmethod
    def contains(self, key):
        pass

    @abc.abstractmethod
    def pprint(self):
        pass

    @abc.abstractmethod
    def entries(self):
        pass
