#include <Arduino.h>
#include <BluetoothSerial.h>

#define LED_BUILTIN 1

BluetoothSerial SerialBT;


void setup()
{
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT);
    SerialBT.begin("Iba-ESP01");
 
}

void loop()
{
    Serial.println("Hello world!");
    SerialBT.println("Hello World");

    delay(1000);

    digitalWrite(LED_BUILTIN, HIGH);
    // wait for a second
    delay(1000);
    // turn the LED off by making the voltage LOW
    digitalWrite(LED_BUILTIN, LOW);
    // wait for a second
    delay(1000);

}
