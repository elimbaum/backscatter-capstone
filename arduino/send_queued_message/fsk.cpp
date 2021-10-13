/* FSK utilities. */

const int CTRL_1_PIN = 10;
const int CTRL_2_PIN = 9;

long count_one, count_zero;

#include "fsk.h"
#include "Arduino.h"

static char serial_buffer[256];

void setup_io() {
  pinMode(CTRL_1_PIN, OUTPUT);
  pinMode(CTRL_2_PIN, OUTPUT);

  digitalWrite(CTRL_1_PIN, LOW);
  digitalWrite(CTRL_2_PIN, LOW);
}

inline void set_count(long c) {
  OCR1A = c;

  // if current count is greater than max val, we won't hit until
  // rollover... so reset.
  // Mod looks cleaner than just setting to zero; tbd.
  if (TCNT1 >= c) {
    TCNT1 = 0;
  }
  
}

long count_from_freq(long freq) {
  return F_CPU / BASEBAND_PRESCALE / 2 / freq - 1;
}

double freq_from_count(long count) {
  return (double)F_CPU / BASEBAND_PRESCALE / 2 / (1 + count);
}

// req_center: requested FSK center frequency, HZ
// req_dev: requested FSK deviation (one-sided), HZ
//
// this function will generate FSK frequencies as close as possible to
// requested, and then adjust center frequency as requred.
void setup_timers(long req_center, long req_dev) {
  long high_count = count_from_freq(req_center + req_dev);
  long low_count = count_from_freq(req_center - req_dev);

  if (high_count == low_count) {
    Serial.println("ERROR! Not enough timer precision. Increase deviation frequency or prescaler.");
    for (;;) { }
  }

  // now that we have counts, figure out what the frequencies actually come out to
  double actual_low_f  = freq_from_count(low_count);
  double actual_high_f = freq_from_count(high_count);

  double actual_center_f = (actual_low_f + actual_high_f) / 2;

  // report back to user
  sprintf(serial_buffer, "Requested %ld +/- %ld Hz", req_center, req_dev);
  Serial.println(serial_buffer);

  Serial.print("Got "); Serial.print(actual_center_f);
  sprintf(serial_buffer, " (+%d, -%d) Hz",
            (int)(actual_high_f - actual_center_f),
            (int)(actual_center_f - actual_low_f));
  Serial.println(serial_buffer);

  sprintf(serial_buffer, "Counts %ld %ld", low_count, high_count);
  Serial.println(serial_buffer);

  count_one = high_count;
  count_zero = low_count;

  ///////////////////////////
  // TURN ON THE TIMERS!
  
  // Set up baseband timer
  // Toggle OC1B (pin 10) on timer compare
  TCCR1A = _BV(COM1B0);
  // CTC with no prescale
  TCCR1B = _BV(WGM12) | _BV(CS10);

  // Set up modulator timer (interrupt)
  TCCR2A = _BV(WGM21); // CTC
  TCCR2B = _BV(CS22); // 64 prescale
  TIMSK2 = _BV(OCIE2A); // interrupt

  set_count(count_zero);

  OCR2A = BIT_OCR;
}

unsigned long b0 = 0;
unsigned long b1 = 0;

void send_bit(char b) {
  if (b) {
    b1++;
    set_count(count_one);
  } else {
    b0++;
    set_count(count_zero);
  }
}
