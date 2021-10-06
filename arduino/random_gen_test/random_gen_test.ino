// Test random vs. python implementation



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  srandom(0);

  Serial.print("Start: "); Serial.println(random());

  for (int i = 0; i < 100; i++) {
    random();
  }

  Serial.print("+100: "); Serial.println(random());


  for (int i = 0; i < 1000; i++) {
    random();
  }

  Serial.print("+1000: "); Serial.println(random());

  for (int i = 0; i < 10000; i++) {
    random();
  }

  Serial.print("+10000: "); Serial.println(random());

  for (int i = 0; i < 10000; i++) {
    random();
  }

  Serial.print("+10000: "); Serial.println(random());
  
}

void loop() {
  // put your main code here, to run repeatedly:


}
