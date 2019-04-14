#include <Arduino.h>
#include "gpio.h"
#include "config.h"

unsigned int relayList[4];


void setup_gpio() {
  
  relayList[0] = RELAY1;
  relayList[1] = RELAY2;
  relayList[2] = RELAY3;
  relayList[3] = RELAY4;

  int length = (sizeof(relayList)/sizeof(*relayList));

  for (int i=0; i < length; i++) {
    pinMode(relayList[i], OUTPUT);
  }

}


void update_gpio(String status) {

  int pinValue = 0;
  int length = (sizeof(relayList)/sizeof(*relayList));

  Serial.println(status);

  for (int i=0; i < length; i++){

    if (status.charAt(i) == '1') {
      pinValue = 0;
    } else {
      pinValue = 1;
    }

    digitalWrite(relayList[i],pinValue);
  }

}




