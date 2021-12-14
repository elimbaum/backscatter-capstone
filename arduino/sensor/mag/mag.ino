
#define MAG_PIN A0

#define AVG_LEN 128

void setup() {
    Serial.begin(115200);
}

void loop() {
    double d = 0;
    for (int i = 0; i < AVG_LEN; i++) {
        d += analogRead(MAG_PIN);
    }
    Serial.println(d / AVG_LEN);
}