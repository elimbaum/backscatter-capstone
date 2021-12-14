#define MAG_PIN A1
#define MIC_PIN A5


#define AVG_LEN 32

void setup() {
    Serial.begin(115200);
}

void loop() {
    double d1 = 0;
    double d2 = 0;

    for (int i = 0; i < AVG_LEN; i++) {
        d1 += analogRead(MAG_PIN);
        d2 += analogRead(MIC_PIN);
    }

    Serial.print(d1 / AVG_LEN);
    Serial.print("\t");
    Serial.println(d2 * 10 / AVG_LEN);
}