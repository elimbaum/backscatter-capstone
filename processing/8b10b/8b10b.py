#!/usr/bin/env python3
#
# 8b10b encoder/decoder
# reads codewords from file

from enum import Enum, auto
from collections import defaultdict, namedtuple
from os import sync
from typing import NamedTuple, Tuple
import random
import sys
from pprint import pprint
import itertools, functools

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

# negative, positive disparity
decodewords = {
    'x': [defaultdict(list), defaultdict(list)],
    'y': [defaultdict(list), defaultdict(list)]
}

# 12 control codes, including commas: K.28.1, K.28.5, K.28.7
CONTROL_CODES = (0x1C, 0x3C, 0x5C, 0x7C, 0x9C, 0xBC,
                 0xDC, 0xFC, 0xF7, 0xFB, 0xFD, 0xFE)

COMMAS = (0x3C, 0xBC) # 0xFC - not using K.28.7 

# these are teh two bit sequences we look for to sync
COMMA_BIT_SEQUENCES = [
    [0, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 0, 1]
]

ENC_RUNNING_DISPARITY = -1

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
    global ENC_RUNNING_DISPARITY

    if rd is None:
        rd = ENC_RUNNING_DISPARITY

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
        
    hi = hi_mapping['x'][x][rd_to_index(ENC_RUNNING_DISPARITY)]
    pc = popcount(hi)
    ENC_RUNNING_DISPARITY += pc - (HI_SIZE - pc)
    
    lo = lo_mapping['y'][y][rd_to_index(ENC_RUNNING_DISPARITY)]
    pc = popcount(lo)
    ENC_RUNNING_DISPARITY += pc - (LO_SIZE - pc)

    res = hi << 4 | lo

    return res

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
        decodewords[f][rd_to_index(-1)][neg_cw].append((v, cw_type))
        decodewords[f][rd_to_index(+1)][pos_cw].append((v, cw_type))
    
# print("data")
# for v in range(0xFF + 1):
#     enc = encode_8b10b(CodewordType.DATA, v)
#     # print(f"{v:3} D.{_8b10b_EDCBA(v):02}.{_8b10b_HGF(v)} {enc:3} ~> {enc:010b}")
#     print(f"{v:3} -> {enc:3} ~ {enc:b}")

# print("control")
# # for v in CONTROL_CODES:
# for v in range(0xFF + 1):
#     enc = encode_8b10b(CodewordType.CONTROL, v)
#     # print(f"{v:3} K.{_8b10b_EDCBA(v):02}.{_8b10b_HGF(v)} {enc:3} ~> {enc:010b}")
#     print(f"{v:3} -> {enc:3} ~ {enc:b}")

ENC_RUNNING_DISPARITY = -1

def random_test():
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

SEED = 13

def bits(b, bitlen=CODEWORD_SIZE):
    # MSB first
    for i in reversed(range(bitlen)):
        yield 1 if (b & (1 << i)) else 0

def random_encoder():
    COMMA_EVERY = 32
    c = 0
    enc_rng = random.Random(SEED)
    while True:
        v = enc_rng.randint(0, 0xFF)
        enc_rng.seed(v * v)

        yield from bits(encode_8b10b(CodewordType.DATA, v))
        c += 1

        if c >= COMMA_EVERY:
            yield from bits(encode_8b10b(CodewordType.CONTROL, COMMAS[0]))
            c = 0

DEC_RUNNING_DISPARITY = -1

def decode_8b10b_symbol(val: int) -> Tuple[CodewordType, int]:
    global DEC_RUNNING_DISPARITY

    hi = val >> 4 # 6 bits abcdei
    dx_opt = decodewords['x'][rd_to_index(DEC_RUNNING_DISPARITY)][hi]
    pc = popcount(hi)
    DEC_RUNNING_DISPARITY += pc - (HI_SIZE - pc)

    lo = val & 0xf # 4 bits fghj 
    dy_opt = decodewords['y'][rd_to_index(DEC_RUNNING_DISPARITY)][lo]
    pc = popcount(lo)
    DEC_RUNNING_DISPARITY += pc - (LO_SIZE - pc)

    # print(f"{hi:06b}, {lo:04b}")

    # decode
    # we take the type of whichever we're forced to (only 1 match)
    if len(dx_opt) == 1:
        dx = dx_opt[0]
        t = dx[1]

        if dy_opt[0][1] == t:
            dy = dy_opt[0]
        else:
            dy = dy_opt[1]

    elif len(dy_opt) == 1:
        dy = dy_opt[0]
        t = dy[1]

        if dx_opt[0][1] == t:
            dx = dx_opt[0]
        else:
            dx = dx_opt[1]
    else:
        raise "uh oh"

    if dy == (8, CodewordType.DATA):
        # D.x.A7 case... make it 7
        dy = (7, CodewordType.DATA)

    return (dy[0] << 5) | dx[0], t

def decode_8b10b_stream(stream_gen):
    global DEC_RUNNING_DISPARITY
    dec_rng = random.Random(SEED)

    stream = stream_gen()

    # eat some random bits
    for _ in range(random.randint(100, 1000)):
        next(stream)

    # first, find comma

    SYNC_LEN = len(COMMA_BIT_SEQUENCES[0])
    sync_window = [0] * SYNC_LEN
    n_comma = 0

    for b in stream:
        n_comma += 1
        
        sync_window.pop(0)
        # append new
        sync_window.append(b)

        if sync_window in COMMA_BIT_SEQUENCES:
            print("Comma after", n_comma)

            # adjust RD
            if sync_window == COMMA_BIT_SEQUENCES[0]:
                # RD was -1, so now 1
                DEC_RUNNING_DISPARITY = 1
            else:
                # was 1, now -1
                DEC_RUNNING_DISPARITY = -1
            
            break
    
    # take two more bits to align with next codeword
    next(stream)
    next(stream)

    n_ok = 0
    n_err = 0

    try:
        for cw_l in itertools.zip_longest(
                    *[iter(stream)] * CODEWORD_SIZE,   
                    fillvalue=0
                ):

            cw = functools.reduce(lambda x, c: (x << 1) | c, cw_l)
            
            v, t = decode_8b10b_symbol(cw)

            if t == CodewordType.CONTROL:
                continue
            
            exp = dec_rng.randint(0, 0xFF)
            dec_rng.seed(v * v)

            try:
                assert v == exp
                n_ok += 1
            except AssertionError:
                print("#")
                n_err += 1
                

    except KeyboardInterrupt:
        print(f"\n== {n_ok} correct")
        print(f"== {n_err} wrong")


def decode_test():
    print("decode test")
    decode_8b10b_stream(random_encoder)

decode_test()