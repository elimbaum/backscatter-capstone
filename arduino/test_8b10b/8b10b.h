#define CODE_DATA (1 << 0)
#define CODE_CTRL (1 << 1)

// partial codeword sizes
#define LO_SIZE 4
#define HI_SIZE 6

// running disparity. starts at -1, recompute after each partial codeword
static int8_t _rd = -1;
#define RD_IDX() ((_rd == -1) ? 0 : 1)

const uint8_t table_5b6b[][2] = {
  {0x27, 0x18},
  {0x1d, 0x22},
  {0x2d, 0x12},
  {0x31, 0x31},
  {0x35, 0x0a},
  {0x29, 0x29},
  {0x19, 0x19},
  {0x38, 0x07},
  {0x39, 0x06},
  {0x25, 0x25},
  {0x15, 0x15},
  {0x34, 0x34},
  {0x0d, 0x0d},
  {0x2c, 0x2c},
  {0x1c, 0x1c},
  {0x17, 0x28},
  {0x1b, 0x24},
  {0x23, 0x23},
  {0x13, 0x13},
  {0x32, 0x32},
  {0x0b, 0x0b},
  {0x2a, 0x2a},
  {0x1a, 0x1a},
  {0x3a, 0x05},
  {0x33, 0x0c},
  {0x26, 0x26},
  {0x16, 0x16},
  {0x36, 0x09},
  {0x0e, 0x0e},
  {0x2e, 0x11},
  {0x1e, 0x21},
  {0x2b, 0x14},
};

const uint8_t table_data_3b4b[][2] = {
  {0x0b, 0x04},
  {0x09, 0x09},
  {0x05, 0x05},
  {0x0c, 0x03},
  {0x0d, 0x02},
  {0x0a, 0x0a},
  {0x06, 0x06},
  {0x0e, 0x01},
  {0x07, 0x08},
};

const uint8_t table_control_3b4b[][2] = {
  {0x0b, 0x04},
  {0x06, 0x09},
  {0x0a, 0x05},
  {0x0c, 0x03},
  {0x0d, 0x02},
  {0x05, 0x0a},
  {0x09, 0x06},
  {0x07, 0x08},
};

uint8_t _encode_hi(uint8_t type, uint8_t x) {
  uint8_t res = 0;
  if (type == CODE_CTRL && x == 28) {
    // K.28 special case
    res = (_rd == -1) ? 0b001111 : 0b110000;
  } else  {
    // all other control codewords reuse data
    res = table_5b6b[x][RD_IDX()];
  }

  uint8_t pc = __builtin_popcount(res);
  // update running disparity with (#1s - #0s)
  _rd += pc - (HI_SIZE - pc);
  return res;
}

// we need to pass in x for the D.x.7 special case
uint8_t _encode_lo(uint8_t type, uint8_t x, uint8_t y) {
  uint8_t res = 0;
  if (type == CODE_DATA) {
    // D.x.P7/A7 special case
    if (y == 7) {
      // we may need to use the alternate.
      bool use_alt = false;
      
      if (_rd == -1 && (x == 17 || x == 18 || x == 20)) {
        use_alt = true;
      }

      if (_rd == 1 && (x == 11 || x == 13 || x == 14)) {
        use_alt = true;
      }

      // we store D.x.P7 at index 7, and D.x.A7 at index 8
      if (use_alt) {
        y = 8;
      }
    }

    res = table_data_3b4b[y][RD_IDX()];
  } else if (type == CODE_CTRL) {
    res = table_control_3b4b[y][RD_IDX()];
  }

  // update rd (res is only one nibble for lo)
  uint8_t pc = __builtin_popcount(res);
  _rd += pc - (LO_SIZE - pc);
  return res;

}

uint16_t encode_8b10b(uint8_t type, uint8_t value) {
  uint8_t x = value & 0x1f;
  uint8_t y = (value >> 5) & 0x7;

  uint8_t hi = _encode_hi(type, x);
  uint8_t lo = _encode_lo(type, x, y);

  return hi << 4 | lo;
}
