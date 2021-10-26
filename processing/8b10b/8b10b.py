#!/usr/bin/env python3
#
# Convert
#   HGF EDCBA
# to
#   abcdei fghj

# output codeword-component bit lengths
BITLEN_X = 6
BITLEN_Y = 4

# pass in RD -1 codeword
class Codeword():
    def __init__(self, cw_str, flip=False):
        bitlen = len(cw_str)
        self.cw = int(cw_str, 2)
        self.mask = (1 << bitlen) - 1
        self.flip = flip
    
    def get(self, rd):
        if rd == -1 or not self.flip:
            return self.cw & self.mask
        elif rd == 1: # and self.flip
            return (~self.cw) & self.mask

class FlipCW(Codeword):
    def __init__(self, cw):
        super().__init__(cw, flip=True)

class SameCW(Codeword):
    pass

# HGF to fghj
table_data_3b4b = {
    "0":  FlipCW("1011"),
    "1":  SameCW("1001"),
    "2":  SameCW("0101"),
    "3":  FlipCW("1100"),
    "4":  FlipCW("1101"),
    "5":  SameCW("1010"),
    "6":  SameCW("0110"),
    "P7": FlipCW("1110"),
    "A7": FlipCW("0111")
}

table_control_3b4b = {
    "0": FlipCW("1011"),
    "1": FlipCW("0110"),
    "2": FlipCW("1010"),
    "3": FlipCW("1100"),
    "4": FlipCW("1101"),
    "5": FlipCW("0101"),
    "6": FlipCW("1001"),
    "7": FlipCW("0111"),
}

# EDCBA to abcdei
# some data and control are shared here
table_data_5b6b = {
    "0":  FlipCW("100111"),
    "1":  FlipCW("011101"),
    "2":  FlipCW("101101"),
    "3":  SameCW("110001"),
    "4":  FlipCW("110101"),
    "5":  SameCW("101001"),
    "6":  SameCW("011001"),
    "7":  FlipCW("111000"),
    "8":  FlipCW("111001"),
    "9":  SameCW("100101"),
    "10": SameCW("010101"),
    "11": SameCW("110100"),
    "12": SameCW("001101"),
    "13": SameCW("101100"),
    "14": SameCW("011100"),
    "15": FlipCW("010111"),
    "16": FlipCW("011011"),
    "17": SameCW("100011"),
    "18": SameCW("010011"),
    "19": SameCW("110010"),
    "20": SameCW("001011"),
    "21": SameCW("101010"),
    "22": SameCW("011010"),
    "23": FlipCW("111010"),
    "24": FlipCW("110011"),
    "25": SameCW("100110"),
    "26": SameCW("010110"),
    "27": FlipCW("110110"),
    "28": SameCW("001110"),
    "29": FlipCW("101110"),
    "30": FlipCW("011110"),
    "31": FlipCW("101011")
}

table_control_5b6b = {
    "28": FlipCW("001111") 
}

for d, cw in table_data_3b4b.items():
    print(d, bin(cw.get(-1)))
    print(" ", d, bin(cw.get(1)))