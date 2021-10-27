#!/usr/bin/env python3
#
# 8b10b encoder/decoder
# reads codewords from file

from enum import Enum, auto
from collections import namedtuple
from typing import NamedTuple

CODEWORD_FILE = '8b10b.tsv'

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


CONTROL_CODES = (0x1C, 0x3C, 0x5C, 0x7C, 0x9C, 0xBC,
                 0xDC, 0xFC, 0xF7, 0xFB, 0xFD, 0xFE)

def _8b10b_HGF(v: int) -> int:
    return (v >> 5) & 0x7

def _8b10b_EDCBA(v: int) -> int:
    return v & 0x1f

def encode_8b10b(cw_type: CodewordType, val: int, rd: int = -1):
    # compute special case for D.x.*7
    # we store this at index 8
    x = _8b10b_EDCBA(val)
    y = _8b10b_HGF(val)
    if y == 7:
        use_alt = (
            (rd == -1 and x in (17, 18, 20))
            or (rd == 1 and x in (11, 13, 14)
        ))
        if use_alt:
            y = 8
    
    mapping = codewords[cw_type]
    rd_idx = 0 if rd == -1 else 1

    lo = mapping['y'][y][rd_idx]
    print(mapping['y'][y])

    # we reuse many of the control chars
    if cw_type == CodewordType.CONTROL and x not in mapping['x']:
        mapping = codewords[CodewordType.DATA]
    hi = mapping['x'][x][rd_idx]
    
    return hi << 4 | lo

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
    
print("data codes")
for v in range(0xFF):
    print("d", v, encode_8b10b(CodewordType.DATA, v, -1))

print("control codes")
for v in CONTROL_CODES:
    enc = encode_8b10b(CodewordType.CONTROL, v, -1)
    print(f"{v:3} K.{_8b10b_EDCBA(v):02}.{_8b10b_HGF(v)} {enc:3} ~> {enc:010b}")
