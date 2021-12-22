
#define MAG_PIN A0

#define AVG_LEN 128

void setup() {
    Serial.begin(115200);
}

void loop() {
    double d = 0;
    long start = micros();
    for (int i = 0; i < AVG_LEN; i++) {
        d += analogRead(MAG_PIN);
    }
    long elapsed = micros() - start;
    Serial.println(d / AVG_LEN);
    // Serial.print("\t");
    // Serial.println(elapsed / AVG_LEN);
}