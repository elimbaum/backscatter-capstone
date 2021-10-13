#define HAMMING_SIZE 7

#define BIT(X, N) (!!(X & _BV(N)))

#define PARITY1(X) (BIT(X, 0) ^ BIT(X, 1) ^             BIT(X, 3))
#define PARITY2(X) (BIT(X, 0) ^             BIT(X, 2) ^ BIT(X, 3))
#define PARITY3(X) (            BIT(X, 1) ^ BIT(X, 2) ^ BIT(X, 3))

//#define HAMMING_CODEWORD(X) (\
//      (BIT(X, 3)  << 6) | \
//      (BIT(X, 2)  << 5) | \
//      (BIT(X, 1)  << 4) | \
//      (PARITY3(X) << 3) | \
//      (BIT(X, 0)  << 2) | \
//      (PARITY2(X) << 1) | \
//      (PARITY1(X) << 0))

#define HAMMING_CODEWORD(X) (\
      (PARITY1(X) << 6) | \
      (PARITY2(X) << 5) | \
      (BIT(X, 0)  << 4) | \
      (PARITY3(X) << 3) | \
      (BIT(X, 1)  << 2) | \
      (BIT(X, 2)  << 1) | \
      (BIT(X, 3)  << 0))      


// map data nibbles to hamming 7-bit codewords
// this is easiest for encode, handle decode all fancy in python.
const int hamming_encode_lut[] = {
    HAMMING_CODEWORD(0x0),
    HAMMING_CODEWORD(0x1),
    HAMMING_CODEWORD(0x2),
    HAMMING_CODEWORD(0x3),
    HAMMING_CODEWORD(0x4),
    HAMMING_CODEWORD(0x5),
    HAMMING_CODEWORD(0x6),
    HAMMING_CODEWORD(0x7),
    HAMMING_CODEWORD(0x8),
    HAMMING_CODEWORD(0x9),
    HAMMING_CODEWORD(0xa),
    HAMMING_CODEWORD(0xb),
    HAMMING_CODEWORD(0xc),
    HAMMING_CODEWORD(0xd),
    HAMMING_CODEWORD(0xe),
    HAMMING_CODEWORD(0xf),
};
