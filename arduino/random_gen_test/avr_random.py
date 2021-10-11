#!/usr/bin/env python3

from itertools import islice

RANDOM_MAX = 0x7FFFFFFF

def skip(g, n):
    return islice(g, n, n + 1)

def avr_random_gen(seed : int):
    next = seed
    
    while True:
        x = next

        if x == 0:
            x = 123459876
        
        hi = x // 127773
        lo = x % 127773
        x = 16807 * lo - 2836 * hi
        if x < 0:
            x += 0x7fffffff
        
        yield x % (RANDOM_MAX + 1)
        next = x

g = avr_random_gen(0)

# print("Start:", next(g))

for _, n in zip(range(100), g):
    print(f"{(n & 0xFF):2X}", end=' ')
