/* ask test with FM0 encoding */

#include "fsk.h"

#define REQUESTED_CENTER_FREQ 161803 // HZ
// #define REQUESTED_CENTER_FREQ 180000
#define LED 13

void setup() {
    Serial.begin(115200);
    Serial.println("\n====");
    Serial.println("ASK/FM0 transmit test\n\n");

    Serial.println("press enter to start...");
    while (! Serial.available()) { }
    Serial.read();

    pinMode(LED, OUTPUT);
    setup_io();
    setup_timers(REQUESTED_CENTER_FREQ);

    Serial.flush();
}

void loop() {
    
}

char last_bit = 0;
char get_bit() {
    return last_bit = ! last_bit;
}

volatile boolean need_new_bit = true;
volatile char bit;

// 1 ms data timer
ISR(TIMER2_COMPA_vect) {
    if (need_new_bit) {
        // get next bit
        bit = get_bit();
        toggle_ask();
        need_new_bit = false;
    } else {
        if (bit == 0) {
            toggle_ask();
        }
        // otherwise (bit == 1) do nothing
        need_new_bit = true;
    }
}