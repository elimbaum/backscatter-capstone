
#define MIC_PIN A2

void setup() {
    Serial.begin(115200);
    analogReference(EXTERNAL);
}

void loop() {
    Serial.println(analogRead(MIC_PIN));
}