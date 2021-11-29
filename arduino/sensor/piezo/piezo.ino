
#define PIEZO_PIN A2

#define AVG_LEN 16

void setup() {
    Serial.begin(115200);
}

void loop() {
    double d = 0;
    for (int i = 0; i < AVG_LEN; i++) {
        d += analogRead(PIEZO_PIN);
    }
    Serial.println(d / AVG_LEN);
}