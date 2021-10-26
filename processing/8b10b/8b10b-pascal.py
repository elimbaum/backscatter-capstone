#!/usr/bin/env python3
#
# 8b10b encoder decoder
#
# SHELVING for now - not worth figuring out from patent.
# This is actually the PHILLIPS implementation; I want IBM to match wikipedia.

from pprint import pprint

# 8 to 10 bit conversion
DATA_BITS        =  8
CODEWORD_BITS    = 10

# absolute value of the allowable disparity
MAX_DISPARITY    =  2

def pascals_triangle(rows, cols, offset=False):
    tri = [[0] * cols]

    # how to determine this?? has to do with RD?
    start = cols // 2 + (1 if offset else 0)
    tri[0][start] = 1

    for r in range(1, rows):
        tri.append([0] * cols)
        for c in range(1, cols):
            tri[r][c] = tri[r - 1][c - 1]

            if c < cols - 1:
                tri[r][c] += tri[r - 1][c + 1]

    return tri

def print_tri(tri, start=None):
    max_n = max(tri[-1])
    fmt_len = len(str(max_n))

    for i in range(len(tri)):
        row = tri[i]
        for j in range(len(row)):
            if row[j]:
                v = row[j]
            else:
                v = ' '
            print(f"{v:{fmt_len}}", end=' ')
        print()

    if start is not None:
        indent = (fmt_len + 1) * start
        print((indent * ' ') + '*' * fmt_len)

def gen_codeword(v, triangle, start=2):
    if len(triangle) == 0:
        return ""

    print("---")
    cmp = triangle[-1][start]
    print(f"cmp {v} to {cmp}")
    print_tri(triangle, start=start)


    if v < cmp:
        print("left")
        return "0" + gen_codeword(v, triangle[:-1], start - 1)
    else:
        print("right")
        return "1" + gen_codeword(v - cmp, triangle[:-1], start + 1)

# print("Generating triangles...")
# print_tri(pascals_triangle(CODEWORD_BITS, 2 * MAX_DISPARITY + 1))
# print("===")
# print_tri(pascals_triangle(CODEWORD_BITS, 2 * MAX_DISPARITY + 1, True))

val = 15

tri = pascals_triangle(CODEWORD_BITS, 2 * MAX_DISPARITY + 1, True)
print("starting triangle1")
print_tri(tri)

cw1 = gen_codeword(val, tri)

# tri = pascals_triangle(CODEWORD_BITS, 2 * MAX_DISPARITY + 1, False)
# print("starting triangle1")
# print_tri(tri, start=1)

cw2 = gen_codeword(val, tri)

print(bin(val), val)
print(cw1, int(cw1, 2))
print(cw2, int(cw2, 2))

