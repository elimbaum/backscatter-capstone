/* FSK utilities - header. */

#ifndef _FSK_H
#define _FSK_H

#define BASEBAND_PRESCALE 1

#define BITS_PER_SECOND 1000
#define BIT_PRESCALE    64
#define BIT_OCR         (F_CPU / BIT_PRESCALE / BITS_PER_SECOND - 1)

// number of groups of preamble symbols to send
// we sent 0xd2, which when hamming encoded is fully alternating
// note 14 bits encoded per byte.
#define NUM_PREAMB  8

long count_from_freq(long freq);
double freq_from_count(long count);

//inline void send_bit(char b);

void setup_io();
void setup_timers(long);

void send_bit(char);

#endif
