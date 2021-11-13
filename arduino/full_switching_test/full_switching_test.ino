/* For testing the RF switch. No data, just basic physical layer.
 */

#include "fsk.h"

static char serial_buffer[256];

#define REQUESTED_CENTER_FREQ 192000
#define LED 13

#define DEBOUNCE_MS 100

void setup() {
    pinMode(LED, OUTPUT);
    setup_io();
    Serial.begin(115200);

    Serial.println("\n============\nRF switch test");
    Serial.println("press enter to start...");
    while (! Serial.available()) { }

    setup_timers(REQUESTED_CENTER_FREQ);

    while (Serial.available()) { Serial.read(); }
    Serial.println("> ");
}

String cmd;

volatile int switching_count = 0;
int switching_interval = 1000;
char curr_bit = 0;

void loop() {
    if (Serial.available()) {
        cmd = Serial.readStringUntil('\n');
        Serial.println(cmd);

        switching_count = 0;
        switching_interval = 0;

        if (cmd == "slow") {
            Serial.println("starting 1 bit/sec");
            switching_interval = 1000;
            digitalWrite(LED, HIGH);
        } else if (cmd == "fast") {
            Serial.println("starting 1000 bit/sec");
            switching_interval = 1;
            digitalWrite(LED, HIGH);
        } else if (cmd == "center") {
            Serial.print("new center freq? > ");
            while (! Serial.available()) { }
            cmd = Serial.readStringUntil('\n');
            Serial.println(cmd);
            unsigned long freq = cmd.toInt();
            setup_timers(freq);
        } else {
            Serial.println("i don't know what that is!");
        }

        Serial.print("> ");
    }

    delay(1);
}

// 1ms timer
ISR(TIMER2_COMPA_vect) {
    if (switching_count % switching_interval == 0) {
        send_bit(curr_bit = !curr_bit);
        switching_count = 0;
    }

    switching_count++;
}