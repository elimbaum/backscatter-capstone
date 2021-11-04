
const int RED_LEN_PIN = 13;
const int GREEN_LEN_PIN = 6;

const int CTRL_1_PIN = 10;
const int CTRL_2_PIN = 9;

const int BUTTON_PIN = 12;

const int BOUNCE_TIME_MS = 50;

#define NOT_PRESSED HIGH
#define PRESSED LOW

void setup() {
    pinMode(RED_LEN_PIN, OUTPUT);
    pinMode(GREEN_LEN_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);

    pinMode(CTRL_1_PIN, OUTPUT);
    pinMode(CTRL_2_PIN, OUTPUT);

    digitalWrite(CTRL_1_PIN, LOW);
    digitalWrite(CTRL_2_PIN, LOW);

    digitalWrite(RED_LEN_PIN, LOW);
    digitalWrite(GREEN_LEN_PIN, HIGH);

    Serial.begin(115200);
}

unsigned long button_count = 0;
boolean button_state = false;
boolean button_toggle = false;

unsigned long start_t = 0;
  
void loop() {
    if (button_state == false && digitalRead(BUTTON_PIN) == PRESSED) {
        // press
        button_state = true;
    } else if (button_state == true && digitalRead(BUTTON_PIN) == NOT_PRESSED) {
        // release
        button_state = false;
        button_count += 1;
        button_toggle = ! button_toggle;
        Serial.println(button_count);
    }

    if (button_toggle) {
        digitalWrite(RED_LEN_PIN, HIGH);
        digitalWrite(GREEN_LEN_PIN, LOW);
        digitalWrite(CTRL_1_PIN, HIGH);
    } else {
        digitalWrite(RED_LEN_PIN, LOW);
        digitalWrite(CTRL_1_PIN, LOW);
        analogWrite(GREEN_LEN_PIN, (millis() / 10) % 255);
    }

}