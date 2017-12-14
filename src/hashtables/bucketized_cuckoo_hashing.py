#!/usr/bin/env python2
from __future__ import print_function
from random import randint
from math import log
import numpy
from itertools import chain

from hashtable import HashTable
from src.util.hash_functions import universal_hash
from src.util.timer import timer


class BucketTable(object):
    """
    Used for the hash tables
    Each table consists of size buckets
    Each bucket is a list of length 9
    bucket[0] next usable index or 5
    bucket[1..4] fields for keys
    bucket[5..8] fields for values
    key bucket[i] and value bucket[i+4] are a pair
    """
    def __init__(self, size):
        self.size = size
        self._table = size * [[]]
        self._hf = universal_hash(size)

    def pprint(self):
        print(self._table)

    def insert(self, key, value):
        addr = self._hf(key)

        try:
            bucket = self._table[addr]
            bucket_index = bucket[0]
        except IndexError:
            bucket = self._table[addr] = [2, key, None, None, None, value, None, None, None]
            return (0, 0)
        
        if bucket_index == 5:
            evicted_key = bucket[1]
            evicted_val = bucket[5]
            self._table[addr][1] = key
            self._table[addr][5] = value
            return (evicted_key, evicted_val)
        else:
            self._table[addr][bucket_index] = key
            self._table[addr][bucket_index + 4] = value
            self._table[addr][0] += 1
            return (0, 0)

    def items(self):
        return (
                (key, bucket[index+4]) 
                    for bucket in self._table
                        for index, key in enumerate(bucket[1:5])
                            if key
               )


class BucketizedCuckooHash(HashTable):
    """
    A variant of Cuckoo Hashing as explained in http://crpit.com/confpapers/CRPITV91Askitis.pdf
    Each slot is a bucket that contains up to four entries
    """
    def __init__(self, size):
        self.size = size
        self._elementcount = 0
        self._maxloop = int(log(size))
        self._table1 = BucketTable(size)
        self._table2 = BucketTable(size)
        self._stash = numpy.full((8192, 2), 0, dtype=numpy.int)
        self._stashf = lambda x : x % 8192

    def insert(self, key, value): # 19,737 s
        for _ in xrange(self._maxloop):
            key, value = self._table1.insert(key, value) # 14 s
            if key == 0:
                self.ckeck_for_rehash_and_resize() # 12 s
                return

            key, value = self._table2.insert(key, value)
            if key == 0:
                self.ckeck_for_rehash_and_resize()
                return

        print("\tStashing key {} and value {}".format(key, value))
        stash_pos = self._stashf(key)
        self._stash[stash_pos][0] = key
        self._stash[stash_pos][1] = value

    def rehash(self):
        entries1 = self._table1.items()
        entries2 = self._table2.items()
        self._elementcount = 0
        self._maxloop = int(log(self.size))
        self._table1 = BucketTable(self.size)
        self._table2 = BucketTable(self.size)

        for key, value in chain(entries1, entries2): 
            self.insert(key, value)

    def ckeck_for_rehash_and_resize(self):
        self._elementcount += 1
        if self._elementcount > 5*self.size:
            print("\tRehashing and Resizing with size={} and elemencount={}".format(self.size, self._elementcount))
            self.size *= 2
            self.rehash()

    def search(self, key):
        pass

    def contains(self, key):
        pass
        
    def tosequence(self):
        pass

    def pprint(self):
        print("-------------- TABLE1")
        # self._table1.pprint()

        print("-------------- TABLE2")
        # self._table2.pprint()

if __name__ == '__main__':
    ht = BucketizedCuckooHash(128)
    for i in range(1, 1000000):
        ht.insert(i,i)
    ht.pprint()
