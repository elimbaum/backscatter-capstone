/* In this version, dynamically generate data, and load it into a queue.
 *  
 * Main loop tries to keep queue load between certain bounds.
 */

#include "fsk.h"
#include "msg_queue.h"
#include "hamming.h"

static char serial_buffer[256];

/* Frequency requests.
 * Timer set up will try to honor these as much as possible, given discrete-timing constraints.
 */
const long REQ_CENTER_FREQ = 200000;
const long REQ_DEV_FREQ    =   5000;

unsigned long start_t;

void setup() {
  Serial.begin(115200);
  Serial.println("\n====");
  Serial.println("backscatter: queued message test\n\n");

  Serial.println("press enter to start...");
  while (! Serial.available()) { }

  pinMode(13, OUTPUT);

  setup_io();
  setup_timers(REQ_CENTER_FREQ, REQ_DEV_FREQ);

  randomSeed(0);
  Serial.flush();

  start_t = millis();
}

extern unsigned long b0, b1;

unsigned char d = 0;

void loop() {
  // put your main code here, to run repeatedly:

  int spots = queue_empty_spots();

//  unsigned long elapsed = millis() - start_t;
//  sprintf(serial_buffer, "Sent %ld bits in %ld ms (%d per)", bits_sent, elapsed, bits_sent / elapsed);

  sprintf(serial_buffer, "0: %ld, 1: %ld, ratio %ld", b0, b1, 100 * b0 / (b0 + b1));
  Serial.println(serial_buffer);

  sprintf(serial_buffer, "Filling %d spots in queue", spots);
 
  Serial.println(serial_buffer);
  for (int i = 0; i < spots; i++) {
    unsigned char r;
//    r = random();
    r = d;
//    r = 0xdd;
    enqueue(r);
    d++;
//    Serial.print(r, HEX); Serial.print(" ");
  }
//  Serial.println();

  delay(QUEUE_REFILL_MS);
}


int8_t bit_index = 0;
uint16_t hamming_data = 0;

ISR(TIMER2_COMPA_vect) {
  // send bits 0..13; at bit_index 14, get a new byte of data.
  // (initially, we'll just send all zeros, that's fine)
  if (bit_index < 0) {
    int d = dequeue();
    
    if (d == QUEUE_EMPTY) {
      // try again next interrupt.
      Serial.println("Q");
//      digitalWrite(13, HIGH);
      return;
    }

    unsigned char ud = d;

//    sprintf(serial_buffer, "Got %x from queue", (unsigned char)d);
//    Serial.println(serial_buffer);
//    
    bit_index = 0;

    // generate hamming-encoded byte
    char hi = ud >> 4;
    char lo = ud & 0xf;

    hamming_data = hamming_encode_lut[hi] << HAMMING_SIZE | hamming_encode_lut[lo];

//    Serial.println(hamming_data, BIN);
    
    bit_index = HAMMING_SIZE * 2 - 1;
  }
//  Serial.println(!!(hamming_data & _BV(bit_index)));
  send_bit(!!(hamming_data & _BV(bit_index)));
  bit_index--;
}
