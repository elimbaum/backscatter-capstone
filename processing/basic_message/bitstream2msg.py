#!/usr/bin/env python3

from pprint import pprint
from itertools import islice

from colorama import Fore, Back, Style

from itertools import zip_longest

import sys
import operator

FILE = sys.argv[1]

PREAMBLE = "1010110011100100"

EXPECTED_MSG = b"The quick brown fox jumped over the lazy dog"

with open(FILE) as f:
    bitstream = f.readline()

print("Looking for", PREAMBLE)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def bin2str(b):
    return bytes(int(b[i : i+8], 2) for i in range(0, len(b), 8))

def partial_decode_print(bytes, expected=None, all_hex=False):
    for i, ch in enumerate(bytes):
        if all_hex or not chr(ch).isprintable():
            if all_hex and not ch:
                print("  ", end='')
            else:
                print(f"{Fore.YELLOW}{ch:02x}{Style.RESET_ALL}", end='')
        else:
            if expected and i < len(expected) and expected[i] != ch:
                print(f"{Back.RED}{chr(ch)} {Style.RESET_ALL}", end='')
            else:
                print(chr(ch), end=' ')
    print()

def count_bits(w : bytes):
    hex_repr = w.hex()
    bin_repr = bin(int(hex_repr, 16))
    return bin_repr.count('1')

def bit_error(exp, act):
    errors = count_bits(bytes(map(operator.xor, byte_res, EXPECTED_MSG)))

    return errors / (8 * len(exp))

# first, naive check: split on the preamble
for w in bitstream.split(PREAMBLE):
    print(f"\n>> message of length {len(w)}")

    # print("out:", w)

    byte_res = bin2str(w)

    ber = bit_error(exp=EXPECTED_MSG, act=byte_res)

    if byte_res.startswith(EXPECTED_MSG):
        print("\tCORRECT")
        assert ber == 0.0
    else:
        print("Got   ", end='')
        partial_decode_print(byte_res, expected=EXPECTED_MSG)
        print("Exp   ", end='')
        partial_decode_print(EXPECTED_MSG)
        print("      ", end='')
        partial_decode_print(
            map(operator.xor, byte_res, EXPECTED_MSG),
            all_hex=True)
        print(f"BER: {ber*100:4.1f} %")

        


    # print(byte_res)
    # print("\t", end='')

    # print()