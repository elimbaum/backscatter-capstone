/* switch states
 *  
 *  State #   C1 C2   Behavior
 *        1    L  L   all ports internal terminated
 *        2    L  H   RF2 to RFCOM, RF1 term
 *        3    H  L   RF1 to RFCOM, RF2 term
 *        4    H  H   ???
 *  For current test, I want state 3 - switch RF1; ignore RF2.
 */

const int CONTROL1_PIN = 10;
const int CONTROL2_PIN = 9;
const int LED_PIN = 13;

void setup() {
  pinMode(CONTROL1_PIN, OUTPUT);
  pinMode(CONTROL2_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(CONTROL1_PIN, LOW);
  digitalWrite(CONTROL2_PIN, LOW);
  digitalWrite(LED_PIN, LOW);

  Serial.begin(115200);
  Serial.println("Start switch test");
}

void loop() {
  digitalWrite(CONTROL1_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(CONTROL1_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  delay(1000);

}
