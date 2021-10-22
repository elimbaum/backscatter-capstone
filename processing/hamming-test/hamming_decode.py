#!/usr/bin/env python3

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
        get_bit(w, 4) << 3 | 
        get_bit(w, 2) << 2 | 
        get_bit(w, 1) << 1 | 
        get_bit(w, 0) << 0
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


def decode(bits, offset, doprint=True):
    out = []
    n_errors = 0
    bits = bits[offset:]
    for sword in chunks(bits, HAMMING_SIZE):
        word = int(sword, 2)
        syn = hamming_syndrome(sword)
        if syn:
            corrected = word ^ (1 << (syn - 1))
            b = hamming_decode(corrected)
            if doprint:
                print(
                    f"{bin(word):>9} ({word:02x}) syn {syn} -> "
                    f"{corrected:02x} =  {b:x}"
                )
            n_errors += 1
        else:
            b = hamming_decode(word)
            if doprint:
                print(
                    f"{bin(word):>9} ({word:02x}) = "
                    f"{b:x}"
                )
        
        out.append(b)

    return n_errors, out

# argmin use
# min(enumerate(a), key=itemgetter(1))[0]
def argmin(L):
    best_i = -1
    best_v = None

    for i, v in enumerate(L):
        if best_v is None or v < best_v:
            best_i = i
            best_v = v

    return best_i

offset_guesses = []

for off in range(HAMMING_SIZE):
    # check hamming against the first chunk of bits
    n_correct, _ = decode(bits[:512], off, doprint=False)
    print(f"offset {off} -> {n_correct} errors")

    offset_guesses.append(n_correct)

best = argmin(offset_guesses)

print("using offset:", best, "\n")

OFFSET = best

n_correct, out = decode(bits, OFFSET, doprint=True)

n_in_pattern = 0
n_bytes = 0

last = None
for i, k in enumerate(chunks(out, 2)):
    if len(k) != 2:
        break

    n_bytes += 1

    full = (k[0] << 4) + k[1]

    if full - 1 == last or (last == 255 and full == 0):
        if correct == False:
            # just moved into a correct region. assume last one was correct.
            n_in_pattern += 1

        correct = True
        # print(Fore.GREEN, end='')
        n_in_pattern += 1
    else:
        correct = False

    # print(f"{i:3} {k[0]:x}{k[1]:x} = {full:3}")

    # print(Style.RESET_ALL, end='')

    last = full

print(f"{n_in_pattern} out of {n_bytes} ({100 * n_in_pattern/n_bytes:.2f}%)")