/* backscatter sensing - full prototype 
 * eli baum // nsap capstone, 2021
 */

#include "fsk.h"
#include "msg_queue.h"

#define REQUESTED_CENTER_FREQ 150000

#define RED_LED 13
#define GREEN_LED 6
#define BUTTON 12
#define MAG_PIN A0

#define MEAS_AVG_LEN 128

#define PACKET_SIZE 16
#define PACKET_NULL 16
#define ACCESS_CODE_LENGTH 4
const uint8_t ACCESS_CODE[ACCESS_CODE_LENGTH] = {0xe1, 0x5a, 0xe8, 0x93};

uint16_t packet_bytes = 0;
uint8_t sqn = 0;

void enqueue_access_code() {
    for (int i = 0; i < ACCESS_CODE_LENGTH; i++) {
        enqueue_block(ACCESS_CODE[i]);
    }
}

// TOOD: add null region before this
void enqueue_packet_header() {
    enqueue_access_code();
    enqueue_block(sqn++);
    enqueue_block(PACKET_SIZE);
}

static char serial_buffer[128];

unsigned long start_t;

void setup() {
    Serial.begin(115200);
    Serial.println(F("\n====\nBackscatter sensing [prototype]"));
    Serial.println(F("NSAP Capstone Project, 2021\n"));
    Serial.println(F("Build " __DATE__ " " __TIME__ "\n"));

    pinMode(BUTTON, INPUT_PULLUP);

    Serial.println(F("Press enter or button to start..."));
    while (! Serial.available() && digitalRead(BUTTON)) { }
    Serial.read();

    pinMode(RED_LED, OUTPUT);
    pinMode(GREEN_LED, OUTPUT);
    digitalWrite(RED_LED, HIGH);

    Serial.println(F("Starting transmit..."));

    setup_io();
    setup_timers(REQUESTED_CENTER_FREQ);

    // preload queue
    enqueue_packet_header();

    start_t = millis();
}

volatile unsigned long sent_bits = 0;
unsigned long num_readings = 0;

void loop() {
    digitalWrite(RED_LED, HIGH);
    // get queue empty spots
    int spots = queue_empty_spots();

    sprintf(serial_buffer, "Filling %d spots", spots);
    Serial.println(serial_buffer);

    for (int i = 0; i < spots; i++) {
        digitalWrite(GREEN_LED, HIGH);
        long r = 0;
        for (int j = 0; j < MEAS_AVG_LEN; j++) {
            r += analogRead(MAG_PIN);
        }
        r /= MEAS_AVG_LEN;
        // TODO: deal with 10 bit issue :)
        enqueue(r >> 2);
        num_readings++;
        packet_bytes++;

        // if we've filled packet, start again
        if (packet_bytes >= PACKET_SIZE) {
            digitalWrite(GREEN_LED, LOW);
            sprintf(serial_buffer, "\t== pkt, last reading %ld ==", r);
            Serial.println(serial_buffer);
            long elapsed = millis() - start_t;
            sprintf(serial_buffer, "\t== %ld bps, %ld meas/sec ==",
                        1000 * sent_bits / elapsed,
                        1000 * num_readings / elapsed);
            Serial.println(serial_buffer);
            enqueue_packet_header();
            packet_bytes = 0;
        }
    }
    digitalWrite(GREEN_LED, LOW);
    
    delay(50);
}



volatile char data_index = 0;
volatile char bit_index = 0;

volatile uint8_t data = 0;

// send data MSB first
inline char get_bit() {
    if (bit_index < 0) {
        int d = dequeue();

        if (d == QUEUE_EMPTY) {
            // Serial.print("Qe");
            digitalWrite(RED_LED, LOW);
            return 0;
        }

        data = (uint8_t) d;

        // data_index++;

        // if (data_index >= ACCESS_CODE_LENGTH) {
        //     data_index = 0;
        // }

        // If I do Hamming, would go here.

        bit_index = 7;
    }

    sent_bits += 1;

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