/* Send a message by modulating a signal.

   In this version, use a timer interrupt for FSK modulation,
   rather than pesky delays.

   Timer 1 handles the baseband
   Timer 2 handles the IRQ and modulation

   Prescale of 64 with count 250 gives exactly 1 kHz.

*/

#include "message.h"

// OC1A: PORT B1 (uno 9) **
// OC1B: PORT B2 (uno 10)

const int CTRL_1_PIN = 10;
const int CTRL_2_PIN = 9;

#define BASEBAND_PRESCALE (1)

#define BITS_PER_SECOND 1000
#define BIT_PRESCALE    64
#define BIT_OCR       (F_CPU / BIT_PRESCALE / BITS_PER_SECOND - 1)

inline void set_count(long c) {
  OCR1A = c;

  // if current count is greater than max val, we won't hit until
  // rollover... so reset.
  // Mod looks cleaner than just setting to zero; tbd.
  if (TCNT1 >= c) {
    TCNT1 %= c;
  }

}

long count_from_freq(long freq) {
  return F_CPU / BASEBAND_PRESCALE / 2 / freq - 1;
}

double freq_from_count(long count) {
  return (double)F_CPU / BASEBAND_PRESCALE / 2 / (1 + count);
}

const long REQ_CENTER_FREQ = 200000;
const long REQ_DEV_FREQ    =   5000;

long count_one, count_zero;

char serial_buffer[256];

#define RADIO_BUFFER_MAX 64

char radio_buffer[RADIO_BUFFER_MAX];

uint16_t rb_index = 0;
uint8_t rb_bit_index = 0;



ISR(TIMER2_COMPA_vect) {
  send_bit(radio_buffer[rb_index] & _BV(rb_bit_index));

  // send MSB to LSB
  if (rb_bit_index == 0) {
    rb_bit_index = 7;
    rb_index++;

    // wrap around if @ end
    if (rb_index >= RADIO_BUFFER_MAX) {
      rb_index = 0;
    }
  } else {
    rb_bit_index--;
  }
}

void setup() {
  // put your setup code here, to run once:
  pinMode(CTRL_1_PIN, OUTPUT);
  pinMode(CTRL_2_PIN, OUTPUT);

  digitalWrite(CTRL_1_PIN, LOW);
  digitalWrite(CTRL_2_PIN, LOW);

  Serial.begin(115200);
  Serial.println("\n\n\n");

  long high_count = count_from_freq(REQ_CENTER_FREQ + REQ_DEV_FREQ);
  long low_count = count_from_freq(REQ_CENTER_FREQ - REQ_DEV_FREQ);
  if (high_count == low_count) {
    Serial.println("ERROR! Not enough timer precision. Increase deviation frequency.");
    for (;;) { }
  }
  double actual_low_f  = freq_from_count(low_count);
  double actual_high_f = freq_from_count(high_count);

  double actual_center_f = (actual_low_f + actual_high_f) / 2;

  sprintf(serial_buffer, "Requested %ld +/- %ld Hz", REQ_CENTER_FREQ, REQ_DEV_FREQ);
  Serial.println(serial_buffer);

  Serial.print("Got "); Serial.print(actual_center_f);
  sprintf(serial_buffer, " (+%d, -%d) Hz",
          (int)(actual_high_f - actual_center_f),
          (int)(actual_center_f - actual_low_f));
  Serial.println(serial_buffer);

  sprintf(serial_buffer, "Counts %ld %ld", low_count, high_count);
  Serial.println(serial_buffer);

  Serial.println("Other options:");
  Serial.println("==Count==Freq======");

  for (long co = high_count - 1; co <= low_count + 1; co++) {
    char flag = ' ';

    if (co == low_count) {
      flag = 'L';
    } else if (co == high_count) {
      flag = 'H';
    }
    // can't printf floats
    sprintf(serial_buffer, "%c %5d  ", flag, co);
    Serial.print(serial_buffer);
    Serial.print(freq_from_count(co));
    Serial.println(" Hz");
  }

  Serial.print("Bit OCR2A: ");
  Serial.println(BIT_OCR);

  sprintf(serial_buffer, "Sending message %s (len %d)",
          MESSAGE,
          strlen(MESSAGE));
  Serial.println(serial_buffer);

  count_one = high_count;
  count_zero = low_count;

  // load up the buffer
  // zero first
  for (int i = 0; i < RADIO_BUFFER_MAX; i++) {
    radio_buffer[i] = 0;
  }

  // load data
  int p = 0;
  // preamble 0xace4, 1010110011100100
  radio_buffer[p++] = (char)0xac;
  radio_buffer[p++] = (char)0xe4;
  strlcpy(&radio_buffer[p], MESSAGE, RADIO_BUFFER_MAX - 2);

  for (int i = 0; i < RADIO_BUFFER_MAX; i++) {
    Serial.println(radio_buffer[i], HEX);
  }

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

  OCR2A = BIT_OCR;
}

//
//inline void send_length() {
//  int msg_len = strlen(MESSAGE);
//  // GNURadio wants it twice
//  send_byte((msg_len >> 8) & 0xFF);
//  send_byte(msg_len & 0xFF);
//  send_byte((msg_len >> 8) & 0xFF);
//  send_byte(msg_len & 0xFF);
//}

void loop() {
  //  Serial.print(rb_index); Serial.print(" "); Serial.println(rb_bit_index);
  //  delay(200);
}
