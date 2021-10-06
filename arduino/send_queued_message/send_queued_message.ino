/* In this version, dynamically generate data, and load it into a queue.
 *  
 * Main loop tries to keep queue load between certain bounds.
 */

#include "fsk.h"
#include "msg_queue.h"

/* Frequency requests.
 * Timer set up will try to honor these as much as possible, given discrete-timing constraints.
 */
const long REQ_CENTER_FREQ = 200000;
const long REQ_DEV_FREQ    =   5000;

void setup() {
  Serial.begin(115200);
  Serial.println("\n====");
  Serial.println("backscatter: queued message test\n\n");

  setup_io();
  setup_timers(REQ_CENTER_FREQ, REQ_DEV_FREQ);
}

void loop() {
  // put your main code here, to run repeatedly:

  delay(QUEUE_REFILL_MS);
}
