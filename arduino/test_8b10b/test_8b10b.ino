#include "8b10b.h"

char serial_buffer[256];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  for (int i = 0; i <= 0xFF; i++) {
    uint16_t e = encode_8b10b(CODE_CTRL, i);
    sprintf(serial_buffer, "%3d -> %3d ~ ", i, e);
    Serial.print(serial_buffer);
    Serial.println(e, BIN);
  }

}

void loop() {

}
