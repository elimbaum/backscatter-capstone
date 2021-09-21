/* Toggle the RF switch a fixed frequency.
 *  
 */

// OC1A: PORT B1 (uno 9) **
// OC1B: PORT B2 (uno 10)

const int CTRL_1_PIN = 10;
const int CTRL_2_PIN = 9;

#define PRESCALE 1

void set_count(long c) {
  OCR1A = c;

  // if current count is greater than max val, we won't hit until
  // rollover... so reset
  if (TCNT1 >= c) {
    TCNT1 = 0;
  }
}

long count_from_freq(long freq) {
  return F_CPU / PRESCALE / 2 / freq - 1;
}

double freq_from_count(long count) {
  return (double)F_CPU / PRESCALE / 2 / (1 + count);
}

const long REQ_CENTER_FREQ = 200000;
const long REQ_DEV_FREQ    =   5000;

long count_a, count_b;

char serial_buffer[256];

void setup() {
  // put your setup code here, to run once:
  pinMode(CTRL_1_PIN, OUTPUT);
  pinMode(CTRL_2_PIN, OUTPUT);

  digitalWrite(CTRL_1_PIN, LOW);
  digitalWrite(CTRL_2_PIN, LOW);

  Serial.begin(115200);
  Serial.println("\n\n\n");

  TCCR1A = 0;
  TCCR1B = 0;

  // Toggle OC1B (pin 10) on timer compare
  TCCR1A |= (1 << COM1B0);
  // CTC with no prescale
  TCCR1B |= (1 << WGM12) | (1 << CS10);

  long high_count = count_from_freq(REQ_CENTER_FREQ + REQ_DEV_FREQ);
  long low_count = count_from_freq(REQ_CENTER_FREQ - REQ_DEV_FREQ);
  if (high_count == low_count) {
    Serial.println("ERROR! Not enough timer precision. Increase deviation frequency.");
    for (;;) { }
  }
  double actual_low_f  = freq_from_count(low_count);
  double actual_high_f = freq_from_count(high_count);

  double actual_center_f = (actual_low_f + actual_high_f) / 2;

  sprintf(serial_buffer, "Requested %ld +/- %ld Hz", REQ_CENTER_FREQ, REQ_DEV_FREQ);
  Serial.println(serial_buffer);

  Serial.print("Got "); Serial.print(actual_center_f);
  sprintf(serial_buffer, " (+ %d, - %d) Hz",
            (int)(actual_high_f - actual_center_f),
            (int)(actual_center_f - actual_low_f));
  Serial.println(serial_buffer);

  sprintf(serial_buffer, "Counts %ld %ld", low_count, high_count);
  Serial.println(serial_buffer);

  Serial.println("Other options:");
  Serial.println("==Count==Freq======");

  for (long co = high_count - 1; co <= low_count + 1; co++) {
    char flag = ' ';

    if (co == low_count) {
      flag = 'L';
    } else if (co == high_count) {
      flag = 'H';
    }
    // can't printf floats
    sprintf(serial_buffer, "%c %5d  ", flag, co);
    Serial.print(serial_buffer);
    Serial.print(freq_from_count(co));
    Serial.println(" Hz");
  }

  count_a = high_count;
  count_b = low_count;
}

const int KEY_TIME_US = 250;

inline void send_zero() {
  set_count(count_a);
  delayMicroseconds(KEY_TIME_US);
  set_count(count_b);
  delayMicroseconds(KEY_TIME_US);
}

inline void send_one() {
  set_count(count_b);
  delayMicroseconds(KEY_TIME_US);
  set_count(count_a);
  delayMicroseconds(KEY_TIME_US);
}

void loop() {
  send_one();
//  send_one();
//  send_zero();
//  send_zero();
//  send_one();
//  send_zero();
}
