/* Similar to original send_queued_message, but now uses 8b10b, rather than
 * hamming, to help with clock sync.
 */

#include <fsk.h>
// #include <8b10b.h>
#include <msg_queue.h>

// #define TX_MSG_INCREMENT
// #define TX_MSG_RANDOM
// #define TX_MSG_CONSTANT

// for sprintf-ing
static char serial_buffer[256];

/* Frequency request
 * Timer will set up the smallest FSK deviation possible near this center
 * frequency as possible.
 */
#define REQUESTED_CENTER_FREQ 200000

unsigned long start_t = 0;

void setup() {
    pinMode(13, OUTPUT);
    setup_io();
    randomSeed(0);

    Serial.begin(115200);

    Serial.println("\n=======================");
    Serial.println("Backscatter Transmitter\n\n");

    Serial.println("press enter to start...");
    while (! Serial.available()) { }

    setup_timers(REQUESTED_CENTER_FREQ);

    Serial.flush();
    start_t = millis();

}

void loop() {

}

ISR(TIMER2_COMPA_vect) {

}