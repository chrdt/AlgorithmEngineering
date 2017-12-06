#!/usr/bin/env python2
from __future__ import print_function
from random import randint
import math

from hashtable import HashTable


class CuckooHash(HashTable):
    def __init__(self, size):
        self.size = size
        self._hf1 = lambda x: self.functionpool()(x) % size
        self._hf2 = lambda x: self.functionpool()(x) % size
        self._table1 = [self.bottom for _ in range(size)]
        self._table2 = [self.bottom for _ in range(size)]
        self._maxloop = int(math.log(size))
        self._elementcount = 0
        self._comp = lambda x, y: True

    def insert(self, key, value):
        # type: (int ,int) -> None
        addr1 = self._hf1(key)
        addr2 = self._hf2(key)

        if self._table1[addr1].key == key:
            print("\tOverwriting key {}".format(key))
            if self._comp(value, self._table1[addr1].value):
                self._table1[addr1] = self.entry(key, value)
            return

        if self._table2[addr2].key == key:
            print("\tOverwriting key {}".format(key))
            if self._comp(value, self._table1[addr2].value):
                self._table1[addr2] = self.entry(key, value)
            return

        for _ in range(self._maxloop):
            hashaddr = self._hf1(key)
            if self._table1[hashaddr] is self.bottom:
                self._table1[hashaddr] = self.entry(key, value)
                self.ckeck_for_rehash_and_resize()
                return
            else:
                newkey = self._table1[hashaddr].key
                newval = self._table1[hashaddr].value
                self._table1[hashaddr] = self.entry(key, value)

            hashaddr = self._hf2(newkey)
            if self._table2[hashaddr] is self.bottom:
                self._table2[hashaddr] = self.entry(newkey, newval)
                self.ckeck_for_rehash_and_resize()
                return
            else:
                key = self._table2[hashaddr].key
                value = self._table2[hashaddr].value
                self._table2[hashaddr] = self.entry(newkey, newval)

        print("\tRehashing after reaching maximal loops")
        self.rehash()
        self.insert(key, value)

    def rehash(self):
        self._hf1 = lambda x: self.functionpool()(x) % self.size
        self._hf2 = lambda x: self.functionpool()(x) % self.size

        insertedpairs = [entry for entry in self._table1 if entry.key] + \
                        [entry for entry in self._table2 if entry.key]

        self._table1 = [self.bottom for _ in range(self.size)]
        self._table2 = [self.bottom for _ in range(self.size)]

        for pair in insertedpairs:
            self.insert(pair.key, pair.value)

    def functionpool(self):
        a = randint(1, self.size-1)
        b = randint(1, self.size-1)
        return lambda x: a*x+b

    def ckeck_for_rehash_and_resize(self):
        self._elementcount += 1
        if self._elementcount > self.size // 2:
            print("\tRehashing and Resizing due to load factor")
            self.size *= 2
            self.rehash()

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

    def tosequence(self):
        # type: () -> str
        res = ''
        for entry in self._table1:
            if entry.key:
                res += str(entry.key) + "\n"
                # res += str(entry.key) + " " + str(entry.value) + "\n"

        for entry in self._table2:
            if entry.key:
                res += str(entry.key) + "\n"
                # res += str(entry.key) + " " + str(entry.value) + "\n"

        return res

if __name__ == '__main__':
    ht = CuckooHash(10)
    ht.pprint()
    for i in range(14):
        ht.insert(i, i)
    ht.pprint()
