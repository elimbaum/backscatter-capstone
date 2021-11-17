/* FSK utilities. */

const int CTRL_1_PIN = 10;
const int CTRL_2_PIN = 9;

long count_one, count_zero;

#include "fsk.h"
#include "Arduino.h"

static char serial_buffer[128];

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

/* setup_timers
 *
 * configure Timer1 for FSK transmission. Will find the closest two FSK
 * frequencies near the requested center frequency.
 * 
 * Note: previous version allowed a requested FSK deviation. Now it will just
 * provide the smallest possible deviation.
 */
void setup_timers(long req_center_f) {
  long requested_count = count_from_freq(req_center_f);
  long possible_center_f = freq_from_count(requested_count);

  unsigned int low_count = 0, high_count = 0;

  // note: +/- backwards because period/freq inverse.
  if (possible_center_f > req_center_f) {
    high_count = requested_count;
    low_count = requested_count + 1;
  } else if (possible_center_f < req_center_f) {
    low_count = requested_count;
    high_count = requested_count - 1;
  } else {
    // on the off chance is exactly right...
    low_count = requested_count + 1;
    high_count = requested_count - 1;
  }

  // now that we have counts, figure out what the frequencies actually are
  double actual_low_f  = freq_from_count(low_count);
  double actual_high_f = freq_from_count(high_count);

  double actual_center_f = (actual_low_f + actual_high_f) / 2;

  // report back to user
  // sprintf(serial_buffer, "Requested center %ld Hz", req_center_f);
  // Serial.println(serial_buffer);

  Serial.print("Got "); Serial.print(actual_center_f);
  sprintf(serial_buffer, " (+%d, -%d) -> (%ld, %ld) Hz",
            (int)(actual_high_f - actual_center_f),
            (int)(actual_center_f - actual_low_f),
            (long)actual_high_f,
            (long)actual_low_f);
  Serial.println(serial_buffer);

  sprintf(serial_buffer, "Counts %d,%d", high_count, low_count);
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

void configure_ask() {
  set_count(count_one);
}

void configure_fsk() {
  TCCR1A = _BV(COM1B0);
}

void send_ask_bit(char b) {
  if (b) {
    b1++;
    TCCR1A = 0;
  } else {
    TCCR1A = _BV(COM1B0);
    b0++;
  }
}

void send_bit(char b) {
  if (b) {
    b1++;
    set_count(count_one);
  } else {
    b0++;
    set_count(count_zero);
  }
}
