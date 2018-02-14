#!/usr/bin/env python2
from __future__ import print_function
from math import log
from itertools import chain

from hashtable import HashTable
from src.util.hash_functions import universal_hash


class CuckooHash(HashTable):
    """
    Pagh and Rodler's Cuckoo Hashing
    Uses a stash for keys that cause irresolvable collisions
    """
    def __init__(self, size):
        self.size = size
        self._elementcount = 0
        self._maxloop = int(log(size))
        self._table1 = [None] * size
        self._table2 = [None] * size
        self._hf1 = universal_hash(size)
        self._hf2 = universal_hash(size)

    def _reset(self):
        self._elementcount = 0
        self._maxloop = int(log(self.size))
        self._table1 = [None] * self.size
        self._table2 = [None] * self.size
        self._hf1 = universal_hash(self.size)
        self._hf2 = universal_hash(self.size)

    def insert(self, key, value):
        addr1 = self._hf1(key)
        addr2 = self._hf2(key)

        if self._table1[addr1].key == key or self._table2[addr2].key == key:
            raise self.InsertionException("Found equal key {}".format(key))

        for _ in range(self._maxloop):
            hashaddr = self._hf1(key)
            if self._table1[hashaddr]:
                oldentry1 = self._table1[hashaddr]
                self._table1[hashaddr] = self.entry(key, value)
            else:
                self._table1[hashaddr] = self.entry(key, value)
                self._ckeck_for_rehash_and_resize()
                return

            hashaddr = self._hf2(oldentry1.key)
            if self._table2[hashaddr]:
                key = self._table2[hashaddr].key
                value = self._table2[hashaddr].value
                self._table2[hashaddr] = oldentry1
            else:
                self._table2[hashaddr] = oldentry1
                self._ckeck_for_rehash_and_resize()
                return

        self._rehash()
        self.insert(key, value)

    def _rehash(self):
        ht1 = (entry for entry in self._table1 if entry)
        ht2 = (entry for entry in self._table2 if entry)
        self._reset()

        for entry in chain(ht1, ht2):
            self.insert(entry.key, entry.value)

    def _ckeck_for_rehash_and_resize(self):
        self._elementcount += 1
        if self._elementcount >= self.size:
            print("\tRehashing and Resizing with size={} and elemencount={}".format(self.size, self._elementcount))
            self.size *= 2
            self.rehash()

    def search(self, key):
        addr1 = self._hf1(key)
        if self._table1[addr1].key == key:
            return self._table1[addr1].value

        addr2 = self._hf2(key)
        if self._table1[addr2].key == key:
            return self._table1[addr2].value

        return None

    def contains(self, key):
        return self._table1[self._hf1(key)].key == key or self._table2[self._hf2(key)].key == key

    def pprint(self):
        print("------ TABLE 1:")
        for index in range(self.size):
            if self._table1[index]:
                field = self._table1[index]
                print("{:^2}: ({:^3}, {:^3})".format(index, field.key, field.value))

        print("\n------ TABLE 2:")
        for index in range(self.size):
            if self._table2[index]:
                field = self._table2[index]
                print("{:^2}: ({:^3}, {:^3})".format(index, field.key, field.value))

    def tosequence(self):
        ht1 = (entry for entry in self._table1 if entry)
        ht2 = (entry for entry in self._table2 if entry)
        items = (str(entry.key) + " " + str(entry.value) for entry in chain(ht1, ht2))
        return "\n".join(items)


if __name__ == '__main__':
    ht = CuckooHash(64)
    for i in range(1000):
        ht.insert(i, i)
    x = ht.tosequence()
