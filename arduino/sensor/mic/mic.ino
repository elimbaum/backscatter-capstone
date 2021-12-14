
#define MIC_PIN A5

#define AVG_LEN 32

void setup() {
    Serial.begin(115200);
}

void loop() {
    double d = 0;
    for (int i = 0; i < AVG_LEN; i++) {
        d += analogRead(MIC_PIN);
    }
    Serial.println(10 * d / AVG_LEN);
}