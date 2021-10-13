import sys
from functools import reduce
import operator as op

FILE = sys.argv[1]

HAMMING_SIZE = 7

def hamming_decode(w):
    # as a string, this is backwards
    return int(w[6] + w[5] + w[4] + w[2], 2)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def hamming_syndrome(w):
    return reduce(
        op.xor,
        (i + 1 for i, bit in enumerate(w) if bit == "1"),
        0
    )

with open(FILE) as f:
    bits = f.read()

for word in chunks(bits, HAMMING_SIZE):
    word = word[::-1]
    syn = hamming_syndrome(word)
    v = int(word, 2)
    if syn:
        print(f"{word} ({v:02x}) syn {syn} -> {v ^ (1 << (syn - 1)):02x}")
    else:
         print(f"{word} ({v:02x}) = {hamming_decode(word):x}")