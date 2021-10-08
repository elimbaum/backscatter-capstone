/* In this version, dynamically generate data, and load it into a queue.
 *  
 * Main loop tries to keep queue load between certain bounds.
 */

#include "fsk.h"
#include "msg_queue.h"


static char serial_buffer[256];

/* Frequency requests.
 * Timer set up will try to honor these as much as possible, given discrete-timing constraints.
 */
const long REQ_CENTER_FREQ = 200000;
const long REQ_DEV_FREQ    =   5000;

void setup() {
  Serial.begin(115200);
  Serial.println("\n====");
  Serial.println("backscatter: queued message test\n\n");

  pinMode(13, OUTPUT);

  setup_io();
  setup_timers(REQ_CENTER_FREQ, REQ_DEV_FREQ);

  randomSeed(0);
  Serial.flush();
}

void loop() {
  // put your main code here, to run repeatedly:

  int spots = queue_empty_spots();
  sprintf(serial_buffer, "Filling %d spots in queue", spots);
  Serial.println(serial_buffer);
  for (int i = 0; i < spots; i++) {
    enqueue(random());
  }

  delay(QUEUE_REFILL_MS);
}


uint8_t bit_index = 0;
uint16_t hamming_data = 0;

#define HAMMING_SIZE 7

// map data nibbles to hamming 7-bit codewords
// this is easiest for encode, handle decode all fancy in python.
uint8_t hamming_encode_lut[] = {
  0b0000000, // 0000
  0b1101001, // 0001
  0b0101010, // 0010
  0b1000011, // 0011
  0b1001100, // 0100
  0b0100101, // 0101
  0b1100110, // 0110
  0b0001111, // 0111
  0b1110000, // 1000
  0b0011001, // 1001
  0b1011010, // 1010
  0b0110011, // 1011
  0b0111100, // 1100
  0b1010101, // 1101
  0b0010110, // 1110
  0b1111111, // 1111
};


ISR(TIMER2_COMPA_vect) {
  // send bits 0..13; at bit_index 14, get a new byte of data.
  // (initially, we'll just send all zeros, that's fine)
  if (bit_index >= HAMMING_SIZE * 2) {
    char d = dequeue();

    if (d == QUEUE_EMPTY) {
      // try again next interrupt.
      digitalWrite(13, HIGH);
      return;
    }
    
    bit_index = 0;
    digitalWrite(13, HIGH);

    // generate hamming
    char hi = d >> 4;
    char lo = d & 0xf;

    hamming_data = hamming_encode_lut[hi] << HAMMING_SIZE | hamming_encode_lut[lo];
    
    if (dequeue() == QUEUE_EMPTY) {
      digitalWrite(13, HIGH);
      Serial.println("EMPTY!");
    } else {
      digitalWrite(13, LOW);
    }
    bit_index = 0;
  }
  send_bit(hamming_data & _BV(bit_index));
  bit_index++;
}
