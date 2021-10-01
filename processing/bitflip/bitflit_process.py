#!/usr/bin/env python3
#
# Testing PREAMBLE + alternating bits (64 pairs)
# So expected message is
#   ACE4 AAAA AAAA ... AAAA (128 bit message)

from pprint import pprint
from itertools import islice

from colorama import Fore, Style

import sys

FILE = sys.argv[1]

PREAMBLE = "1010110011100100"

EXPECTED_N_BITS = 128 + 16

with open(FILE) as f:
    bitstream = f.readline()

print("Looking for", PREAMBLE)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def bin2str(b):
    return bytes(int(b[i : i+8], 2) for i in range(0, len(b), 8))

total_bits = 0
good_bits = 0

# first, naive check: split on the preamble
for w in bitstream.split(PREAMBLE):
    print(f"\n>>      message of length {len(w)} ({len(w) / EXPECTED_N_BITS:.5} bitstream-lengths)")

    last = None
    for b in w:
        if b == last:
            print(Fore.RED, b, sep='', end='')
        else:
            print(Style.RESET_ALL, b, sep='', end='')
            good_bits += 1
        total_bits += 1
        last = b

    print(Style.RESET_ALL)

    # for off in range(8):
    #     byte_res = bin2str(out[off:])
    #     try:
    #         print(byte_res.decode())
    #     except UnicodeDecodeError:
    #         print("\t ## ", byte_res)

print(f"{good_bits}/{total_bits} = {100 * good_bits/total_bits:.5}% good")