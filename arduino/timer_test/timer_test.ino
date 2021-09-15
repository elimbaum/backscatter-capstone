const int LED_PIN = 13;

// OC0A: PORT D6 (arduino uno 6)
// OC0B: PORT D5 (arduino uno 5)

// OC1A: PORT B1 (uno 9) **
// OC1B: PORT B2 (uno 10)


#define PRESCALE 1

#define PRINT_REG(reg) (Serial.print(#reg ": "), Serial.println(reg, BIN))

void set_freq(long f) {
  OCR1A = F_CPU / PRESCALE / 2 / f - 1;
}

void setup() {  
  Serial.begin(9600);
  Serial.println("===");
  
  DDRB |= (1 << DDB1);

  TCCR1A = 0;
  TCCR1B = 0;

  // Toggle OC1A (pin 9) on timer compare
  TCCR1A |= (1 << COM1A0);
  // CTC with no prescale
  TCCR1B |= (1 << WGM12) | (1 << CS10);
  // Set compare register - toggle at freq
//  OCR1A = F_CPU / PRESCALE / 2 / FREQ_HZ - 1;


  PRINT_REG(TCCR1A);
  PRINT_REG(TCCR1B);
  PRINT_REG(OCR1A);
  Serial.print(OCR1A);
}


#define FREQ_A 100000
#define FREQ_B 150000
#define STEP_SIZE ((FREQ_B - FREQ_A) / 100);

long f = FREQ_A;
long step = STEP_SIZE;

void loop() {
  if (f < FREQ_A) {
    step = STEP_SIZE;
    f = FREQ_A;
  } else if (f > FREQ_B) {
    step = -STEP_SIZE;
    f = FREQ_B;
  }

  set_freq(f);
  f += step;
  delay(1);

  Serial.println(f);
}
