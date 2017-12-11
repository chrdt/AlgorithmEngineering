#!/usr/bin/env python2
from __future__ import print_function
from random import randint
from math import log

from hashtable import HashTable
from src.util.hash_functions import universal_hash


class CuckooHash(HashTable):
    def __init__(self, size):
        self.size = size
        self._elementcount = 0
        self._maxloop = int(log(size))
        self._table2 = []
        self._table1 = []
        self._hf2 = universal_hash(size)
        self._hf1 = universal_hash(size)

    def reset(self):
        self._elementcount = 0
        self._maxloop = int(log(self.size))
        self._table2 = []
        self._table1 = []
        self._hf2 = universal_hash(self.size)
        self._hf1 = universal_hash(self.size)

    def insert(self, key, value):
        addr1 = self._hf1(key)
        addr2 = self._hf2(key)

        if self._table1[addr1].key == key:
            print("\tFound equal key {}".format(key))
            # TODO: compare values here
            return

        if self._table2[addr2].key == key:
            print("\tFound equal key {}".format(key))
            # TODO: compare values here
            return

        for _ in range(self._maxloop):
            hashaddr = self._hf1(key)

            try:
                oldkey = self._table1[hashaddr].key
                oldval = self._table1[hashaddr].value
                self._table1[hashaddr] = self.entry(key, value)
            except IndexError:
                self._table1[hashaddr] = self.entry(key, value)
                self.ckeck_for_rehash_and_resize()
                return

            hashaddr = self._hf2(oldkey)
            try:
                key = self._table2[hashaddr].key
                value = self._table2[hashaddr].value
                self._table2[hashaddr] = self.entry(oldkey, oldval)
            except IndexError:
                self._table2[hashaddr] = self.entry(oldkey, oldval)
                self.ckeck_for_rehash_and_resize()
                return

        print("\tRehashing after reaching maximal loops")
        self.rehash()
        self.insert(key, value)

    def rehash(self):
        ht1 = self._table1[:]
        ht2 = self._table2[:]
        self.reset()

        for entry in ht1 + ht2:
            self.insert(entry.key, entry.value)

    def ckeck_for_rehash_and_resize(self):
        self._elementcount += 1
        if self._elementcount > self.size // 2:
            print("\tRehashing and Resizing due to load factor {}".format(self.size//self._elementcount))
            self.size *= 2
            self.rehash()

    def search(self, key):
        addr1 = self._hf1(key)
        addr2 = self._hf2(key)

        if self._table1[addr1].key == key:
            return self._table1[addr1].value

        if self._table1[addr2].key == key:
            return self._table1[addr2].value

        return -1

    def contains(self, key):
        return self._table1[self._hf1(key)].key == key or self._table2[self._hf2(key)].key == key

    def pprint(self):
        print("------ TABLE 1:")
        for i in range(self.size):
            field = self._table1[i]
            print("{:^2}: ({:^3}, {:^3})".format(i, field.key, field.value))

        print("\n------ TABLE 2:")
        for i in range(self.size):
            field = self._table2[i]
            print("{:^2}: ({:^3}, {:^3})".format(i, field.key, field.value))

    def tosequence(self):
        res = ''
        for entry in self._table1:
            if entry.key:
                res += str(entry.key) + "\n"

        for entry in self._table2:
            if entry.key:
                res += str(entry.key) + "\n"

        return res


if __name__ == '__main__':
    ht = CuckooHash(10)
    ht.pprint()
    for i in range(14):
        ht.insert(i, i)
    ht.pprint()
