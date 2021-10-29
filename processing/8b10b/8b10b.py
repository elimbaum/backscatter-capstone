#!/usr/bin/env python3
#
# 8b10b encoder/decoder
# reads codewords from file

from enum import Enum, auto
from collections import namedtuple
from typing import NamedTuple, Tuple
from random import randint
import sys

CODEWORD_FILE = '8b10b.tsv'

HI_SIZE = 6
LO_SIZE = 4
CODEWORD_SIZE = HI_SIZE + LO_SIZE

class CodewordType(Enum):
    CONTROL = auto()
    DATA = auto()

codewords = {
    CodewordType.DATA: {
        'x': {},
        'y': {}
    },
    CodewordType.CONTROL: {
        'x': {},
        'y': {}
    }
}

# 12 control codes, including commas: K.28.1, K.28.5, K.28.7
CONTROL_CODES = (0x1C, 0x3C, 0x5C, 0x7C, 0x9C, 0xBC,
                 0xDC, 0xFC, 0xF7, 0xFB, 0xFD, 0xFE)

RUNNING_DISPARITY = -1

def _8b10b_HGF(v: int) -> int:
    return (v >> 5) & 0x7

def _8b10b_EDCBA(v: int) -> int:
    return v & 0x1f

def popcount(b: int) -> int:
    return bin(b).count('1')

# look up in tuple
def rd_to_index(rd: int) -> int:
    if rd == -1:
        return 0
    elif rd == 1:
        return 1

def encode_8b10b(cw_type: CodewordType, val: int, rd: int = None):
    global RUNNING_DISPARITY

    if rd is None:
        rd = RUNNING_DISPARITY

    # compute special case for D.x.*7
    # we store this at index 8
    x = _8b10b_EDCBA(val)
    y = _8b10b_HGF(val)

    # print("D", x, y)

    if cw_type == CodewordType.DATA and y == 7:
        use_alt = (
            (rd == -1 and x in (17, 18, 20))
            or (rd == 1 and x in (11, 13, 14)
        ))
        if use_alt:
            y = 8
    
    hi_mapping = lo_mapping = codewords[cw_type]

    # we reuse many of the control chars
    if cw_type == CodewordType.CONTROL and x not in hi_mapping['x']:
        hi_mapping = codewords[CodewordType.DATA]
        
    hi = hi_mapping['x'][x][rd_to_index(RUNNING_DISPARITY)]
    pc = popcount(hi)
    RUNNING_DISPARITY += pc - (HI_SIZE - pc)
    
    lo = lo_mapping['y'][y][rd_to_index(RUNNING_DISPARITY)]
    pc = popcount(lo)
    RUNNING_DISPARITY += pc - (LO_SIZE - pc)

    res = hi << 4 | lo

    return res

def decode_8b10b(val: int, rd: int = None) -> Tuple[CodewordType, int]:
    # do we need to have a separate running disparity here?
    pass

with open(CODEWORD_FILE) as f:
    header = f.readline().split()
    assert header == ['DATA', 'CODE', 'OTHER_CODE']

    for line in f:
        fields = line.split()
        d = fields[0]
        cw_str = fields[1]

        bitlen = len(cw_str)
        mask = (1 << bitlen) - 1

        pos_cw = neg_cw = int(cw_str, 2)

        if len(fields) == 3 and fields[2] == 'FLIP':
            pos_cw = (~neg_cw) & mask

        cw_comp = d.split('.')

        if cw_comp[0] == 'D':
            cw_type = CodewordType.DATA
        elif cw_comp[0] == 'K':
            cw_type = CodewordType.CONTROL

        # we store in the opposite of the field that is printed
        # i.e. D.x.7 is a codeword for the *y* dictionary, and vice versa
        if cw_comp[1] == 'x':
            f = 'y'
            if cw_comp[2] == 'P7':
                v = 7
            elif cw_comp[2] == 'A7':
                v = 8
            else:
                v = int(cw_comp[2])
        elif cw_comp[2] == 'y':
            f = 'x'
            v = int(cw_comp[1])

        codewords[cw_type][f][v] = (neg_cw, pos_cw)
    
print("data")
for v in range(0xFF + 1):
    enc = encode_8b10b(CodewordType.DATA, v)
    # print(f"{v:3} D.{_8b10b_EDCBA(v):02}.{_8b10b_HGF(v)} {enc:3} ~> {enc:010b}")
    print(f"{v:3} -> {enc:3} ~ {enc:b}")

print("control")
# for v in CONTROL_CODES:
for v in range(0xFF + 1):
    enc = encode_8b10b(CodewordType.CONTROL, v)
    # print(f"{v:3} K.{_8b10b_EDCBA(v):02}.{_8b10b_HGF(v)} {enc:3} ~> {enc:010b}")
    print(f"{v:3} -> {enc:3} ~ {enc:b}")

RUNNING_DISPARITY = -1

print("starting random test")
stream = []
n_check = 0
last_check = 0
while True:
    v = randint(0, 0xFF)
    enc = encode_8b10b(CodewordType.DATA, v)
    stream.append(enc)

    bin_stream = ''.join(f"{e:010b}" for e in stream)
    # print(bin_stream)

    try:
        assert "0" * 6 not in bin_stream
        assert "1" * 6 not in bin_stream
        assert "00111110" not in bin_stream
        assert "11000001" not in bin_stream
    except AssertionError:
        print(bin_stream)
        print(n_check, "were ok")
        break

    n_check += 1

    if len(stream) > 4:
        stream.pop(0)

    if n_check >= last_check * 8:
        print(n_check, "checked, ok")
        last_check = n_check

    