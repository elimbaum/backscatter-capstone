/* FSK utilities - header. */

#ifndef _FSK_H
#define _FSK_H

#define BASEBAND_PRESCALE 1

#define SYMB_PER_SECOND 2000
#define FM0_BITS_PER_SECOND (SYMB_PER_SECOND / 2)
#define SYMB_PRESCALE    64
#define SYMB_OCR         (F_CPU / SYMB_PRESCALE / SYMB_PER_SECOND - 1)

// number of groups of preamble symbols to send
// we sent 0xd2, which when hamming encoded is fully alternating
// note 14 bits encoded per byte.
#define NUM_PREAMB  8

long count_from_freq(long freq);
double freq_from_count(long count);

//inline void send_bit(char b);

void setup_io();
void setup_timers(long);

void configure_ask(void);
void configure_fsk(void);

void send_ask_bit(char);
void toggle_ask(void);
void send_bit(char);

#endif
