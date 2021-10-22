#!/usr/bin/env python3
#
# 8b10b encoder decoder

from pprint import pprint

# 8 to 10 bit conversion
DATA_BITS        =  8
CODEWORD_BITS    = 10

# absolute value of the allowable disparity
MAX_DISPARITY    = 2

def pascals_triangle(rows, cols):
    tri = [[0] * cols]

    start = cols // 2 + 1
    tri[0][start] = 1

    for r in range(1, rows):
        tri.append([0] * cols)
        for c in range(1, cols):
            tri[r][c] = tri[r - 1][c - 1]

            if c < cols - 1:
                tri[r][c] += tri[r - 1][c + 1]

    return tri

def print_tri(tri):
    max_n = max(tri[-1])
    fmt_len = len(str(max_n))

    for i in range(len(tri)):
        row = tri[i]
        for j in range(1, len(row)):
            if row[j]:
                v = row[j]
            else:
                v = ' '
            print(f"{v:{fmt_len}}", end=' ')
        print()

print_tri(pascals_triangle(CODEWORD_BITS, 2 * MAX_DISPARITY + 1))
