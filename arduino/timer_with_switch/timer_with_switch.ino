/* Toggle the RF switch a fixed frequency.
 *  
 */

// OC1A: PORT B1 (uno 9) **
// OC1B: PORT B2 (uno 10)

const int CTRL_1_PIN = 10;
const int CTRL_2_PIN = 9;

#define PRESCALE 1

void set_freq(long f) {
  OCR1A = F_CPU / PRESCALE / 2 / f - 1;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(CTRL_1_PIN, OUTPUT);
  pinMode(CTRL_2_PIN, OUTPUT);

  digitalWrite(CTRL_1_PIN, LOW);
  digitalWrite(CTRL_2_PIN, LOW);

  TCCR1A = 0;
  TCCR1B = 0;

  // Toggle OC1B (pin 10) on timer compare
  TCCR1A |= (1 << COM1B0);
  // CTC with no prescale
  TCCR1B |= (1 << WGM12) | (1 << CS10);

  set_freq(100000);
}

const long f_a =  75000;
const long f_b   = 125000;

void loop() {
  set_freq(f_a);
  delay(1000);
  set_freq(f_b);
  delay(1000);
}
