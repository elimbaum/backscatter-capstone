#!/usr/bin/env python3

from pprint import pprint
from itertools import islice

FILE = "bitstream_wired_message.txt"

PREAMBLE = "111101"

phy_bit_map = {
    0: "10",
    1: "01"
}

bit_phy_map = {
    "10": "0",
    "01": "1"
}

preamble_phy = ''.join(list(map(lambda x: phy_bit_map[int(x)], PREAMBLE)))

with open(FILE) as f:
    bitstream = f.readline()

print("Looking for", preamble_phy)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def bin2str(b):
    return bytes(int(b[i : i+8], 2) for i in range(0, len(b), 8))

# first, naive check: split on the preamble
for w in bitstream.split(preamble_phy):
    print(f"message of length {len(w)}")

    g = iter(w)
    out = ""

    try:
        while True:
            b = next(g) + next(g)

            while b not in bit_phy_map:
                b = b[0] + next(g)


            out += bit_phy_map[b]
    except StopIteration:
        pass

    print("out:", out)

    # for off in range(8):
    #     byte_res = bin2str(out[off:])
    #     try:
    #         print(byte_res.decode())
    #     except UnicodeDecodeError:
    #         print("\t ## ", byte_res)