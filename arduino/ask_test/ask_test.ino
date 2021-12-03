/* ask test with FM0 encoding */

#include "fsk.h"

#define REQUESTED_CENTER_FREQ 190000 // HZ
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

volatile boolean start_of_bit = true;
volatile char bit;

// 1 ms data timer
ISR(TIMER2_COMPA_vect) {
    if (start_of_bit) {
        // get next bit
        bit = get_bit();
        toggle_ask();
        start_of_bit = true;
    } elif (bit == 0) {
        toggle_ask();
        start_of_bit = false;
    }
}