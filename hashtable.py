#!/usr/bin/env python2
import abc
from collections import namedtuple


class HashTable(object):
    __metaclass__ = abc.ABCMeta
    entry = namedtuple("entry", ["key", "value"])

    def bottom(self):
        # type: () -> object
        return None

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


class CuckooHash(HashTable):
    def __init__(self, size, hashfunction1=lambda x: x, hashfunction2=lambda x: x):
        self.size = size
        self._hf1 = lambda x: hashfunction1(x) % size
        self._hf2 = lambda x: hashfunction2(x) % size
        self._table1 = [self.entry(self.bottom(), self.bottom()) for _ in range(size)]
        self._table2 = [self.entry(self.bottom(), self.bottom()) for _ in range(size)]
        self._maxloop = size**2

    def insert(self, key, value):
        # type: (int ,int) -> None
        if self.contains(key):
            print("Already inserted")
            return

        for _ in range(self._maxloop):
            hashaddr = self._hf1(key)
            if self._table1[hashaddr].key:
                newkey = self._table1[hashaddr].key
                newval = self._table1[hashaddr].value
                self._table1[hashaddr] = self.entry(key, value)
            else:
                self._table1[hashaddr] = self.entry(key, value)
                return

            hashaddr = self._hf2(newkey)
            if self._table2[hashaddr].key:
                key = self._table2[hashaddr].key
                val = self._table2[hashaddr].value
                self._table2[hashaddr] = self.entry(newkey, newval)
            else:
                self._table2[hashaddr] = self.entry(newkey, newval)
                return

        print("Reached maximal Loops")

    def delete(self, key):
        # type: (int) -> None
        pass

    def search(self, key):
        # type: (int) -> int
        addr1 = self._hf1(key)
        addr2 = self._hf2(key)

        if self._table1[addr1].key == key:
            return self._table1[addr1].value

        if self._table1[addr2].key == key:
            return self._table1[addr2].value

        return -1

    def contains(self, key):
        addr1 = self._hf1(key)
        addr2 = self._hf2(key)

        return self._table1[addr1].key == key or self._table2[addr2].key == key

    def pprint(self):
        # type: () -> None
        print("------ TABLE 1:")
        for i in range(self.size):
            field = self._table1[i]
            print("{:^2}: ({:^3}, {:^3})".format(i, field.key, field.value))

        print("\n------ TABLE 2:")
        for i in range(self.size):
            field = self._table2[i]
            print("{:^2}: ({:^3}, {:^3})".format(i, field.key, field.value))


class SimpleHash(HashTable):
    def __init__(self, size):
        self.size = size
        self._table = [[-1, -1] for _ in range(size)]
        self._hashfunction = lambda x: x

    def insert(self, key, value):
        hashadr = self._hashfunction(key)
        self._table[hashadr][0] = key
        self._table[hashadr][1] = value

    def delete(self, key):
        hashadr = self._hashfunction(key)
        self._table[hashadr][0] = -1
        self._table[hashadr][1] = -1

    def search(self, key):
        hashadr = self._hashfunction(key)
        return self._table[hashadr][1]

    def pprint(self):
        for i in range(self.size):
            obj = self._table[i]
            print("{:^2}: ({:^3}, {:^3})".format(i, obj[0], obj[1]))


ht = CuckooHash(10)
ht.pprint()
for i in range(14):
    ht.insert(i, i)
ht.pprint()
