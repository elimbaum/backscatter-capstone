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

ISR(TIMER2_COMPA_vect) {
  if (bit_index == 7) {
//    Serial.println(queue_count());
    if (dequeue() == QUEUE_EMPTY) {
      digitalWrite(13, HIGH);
      Serial.println("EMPTY!");
    } else {
      digitalWrite(13, LOW);
    }
    bit_index = 0;
  } else {
    bit_index++;
  }
}
