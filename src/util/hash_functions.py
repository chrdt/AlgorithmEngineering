#!/usr/bin/env python2
from __future__ import print_function

from random import randint
from math import sqrt


def multiplicative_hash(x, p=0):
    """
    Uses Knuth's multiplicative hashing
    :param x: integer that is to be hashed
    :param p: integer that parametrizes the shift
    :return: hash value of x
    """
    assert 0 <= p <= 32

    knuth = long(2654435761)
    y = long(x)
    return (y * knuth) >> (32 - p)  # TODO: needs modulo or sth


def universal_hash(m):
    """
    Uses Universal hashing
    :param m: the length of the hash table
    :return: a random hash function
    """
    p = next_prime(m)
    a = randint(1, p - 1)
    b = randint(1, p - 1)
    return lambda x: ((a * x + b) % p) % m


def next_prime(n):
    """
    better approach: https://stackoverflow.com/a/5694432/6257606
    :param n: integer
    :return: a prime that is larger than n
    """
    p = n+1
    q = n * 3
    for _ in xrange((q - p) ** 2 + 20):
        i = randint(p, q) | 1
        if is_prime(i):
            return i


def is_prime(n):
    """
    Uses the fact that primes are neighbours of multiples of 6
    might be better: Miller-Rabin-Test
    :param n: integer to be checked
    :return: True if n is a prime
    """
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w

    return True


def sieve_of_atkin(limit):
    """
    In case I want to calculate all primes before running the algorithm
    :param limit: upper limit
    :return: a list of all primes (0, limit]
    """
    primes = [2, 3]
    sieve = [False] * (limit + 1)

    for x in xrange(1, int(sqrt(limit)) + 1):
        for y in xrange(1, int(sqrt(limit)) + 1):
            n = 4 * x**2 + y**2
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                sieve[n] = not sieve[n]

            n = 3 * x ** 2 + y ** 2
            if n <= limit and n % 12 == 7:
                sieve[n] = not sieve[n]

            n = 3 * x ** 2 - y ** 2
            if x > y and n <= limit and n % 12 == 11:
                sieve[n] = not sieve[n]

    for x in xrange(5, int(sqrt(limit))):
        if sieve[x]:
            for y in xrange(x ** 2, limit + 1, x ** 2):
                sieve[y] = False

    for p in xrange(5, limit):
        if sieve[p]:
            primes.append(p)

    return primes
