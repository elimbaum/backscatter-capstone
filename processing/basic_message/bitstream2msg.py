#!/usr/bin/env python3

from pprint import pprint
from itertools import islice

from colorama import Fore, Style

import sys

FILE = sys.argv[1]

PREAMBLE = "1010110011100100"

EXPECTED_MSG = "The quick brown fox jumped over the lazy dog."

with open(FILE) as f:
    bitstream = f.readline()

print("Looking for", PREAMBLE)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def bin2str(b):
    return bytes(int(b[i : i+8], 2) for i in range(0, len(b), 8))

# first, naive check: split on the preamble
for w in bitstream.split(PREAMBLE):
    print(f"\n>> message of length {len(w)}")

    # print("out:", w)

    byte_res = bin2str(w)
    print("\t", end='')
    for ch in byte_res:
        if not chr(ch).isprintable():
            print(Fore.RED + '?' + Style.RESET_ALL, end='')
        else:
            print(chr(ch), end='')
    print()