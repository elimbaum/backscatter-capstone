import sys
from functools import reduce
import operator as op

from colorama import Fore, Back, Style

FILE = sys.argv[1]

HAMMING_SIZE = 7

def get_bit(v, i):
    return (v & (1 << i)) != 0

def hamming_decode(w):
    return (
        get_bit(w, 4) << 0 | 
        get_bit(w, 2) << 1 | 
        get_bit(w, 1) << 2 | 
        get_bit(w, 0) << 3
    )

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def hamming_syndrome(w):
    w = list(map(int, w))
    return reduce(
        op.xor,
        (i + 1 for i, bit in enumerate(w) if bit),
        0
    )

with open(FILE) as f:
    bits = f.read()

out = []

for sword in chunks(bits, HAMMING_SIZE):
    word = int(sword[::-1], 2)
    syn = hamming_syndrome(sword)
    if syn:
        corrected = word ^ (1 << (syn - 1))
        b = hamming_decode(corrected)
        print(f"{bin(word):>9} ({word:02x}) syn {syn} -> {corrected:02x} =  "
              f"{b:x}")
    else:
        b = hamming_decode(word)
        print(f"{bin(word):>9} ({word:02x}) =              "
              f"{b:x}")
    
    out.append(b)

last = None
for i, k in enumerate(chunks(out, 2)):
    full = (k[0] << 4) + k[1]

    correct = False
    if full - 1 == last:
        correct = True
        print(Fore.GREEN, end='')
        
    print(f"{i:3} {k[0]:x}{k[1]:x} = {full:3}")

    print(Style.RESET_ALL, end='')

    last = full