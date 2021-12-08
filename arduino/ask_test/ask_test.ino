/* ask test with FM0 encoding */

#include "fsk.h"

// #define REQUESTED_CENTER_FREQ 161803 // HZ
#define REQUESTED_CENTER_FREQ 150000
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

volatile uint8_t data = 0;
volatile char bit_index = 0;

// send data MSB first
inline char get_bit() {
    if (bit_index < 0) {
        data++;
        bit_index = 7;
    }

    char b = !!(data & _BV(bit_index));
    bit_index--;
    return b;
}

volatile boolean need_new_bit = true;
volatile char bit;

/* 1 ms data timer
 * actually on sending one full bit every other, since we need the
 * intra-symbol transition
 *
 * 0 = short short
 * 1 = long
 */
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