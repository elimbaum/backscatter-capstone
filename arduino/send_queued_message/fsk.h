/* FSK utilities - header. */

#define BASEBAND_PRESCALE 1

#define BITS_PER_SECOND 1000
#define BIT_PRESCALE    64
#define BIT_OCR       (F_CPU / BIT_PRESCALE / BITS_PER_SECOND - 1)

long count_from_freq(long freq);
double freq_from_count(long count);

//inline void send_bit(char b);

void setup_io();
void setup_timers(long, long);
