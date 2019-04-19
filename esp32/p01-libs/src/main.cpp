#include <Arduino.h>

#define RELAY01 25
#define RELAY02 26
#define RELAY03 27


void setup() {
    Serial.begin(9600);
 
    pinMode(RELAY01, OUTPUT);
    pinMode(RELAY02, OUTPUT);
    pinMode(RELAY03, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {
    Serial.println("Hello world!");
    delay(1000);

    digitalWrite(RELAY01, LOW);
    digitalWrite(RELAY02, LOW);
    digitalWrite(RELAY03, LOW);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);

    // turn the LED off 
    digitalWrite(RELAY01, HIGH);
    digitalWrite(RELAY02, HIGH);
    digitalWrite(RELAY03, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);

}
