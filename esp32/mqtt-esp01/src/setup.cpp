#include <Arduino.h>
#include <ESP8266WiFi.h>

#include "setup.h"
#include "secrets.h"
#include "config.h"

String mac;


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  mac = WiFi.macAddress();
  Serial.print("WiFi MAC: ");
  Serial.println(mac);

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}



void set_clientId(char * clientId) {

  strcpy(clientId,MQTT_CLIENT_ID);
  int length = mac.length();
  int pos = strlen(clientId);

  for (int i = 0; i < length ; i++) {

    if ((char)mac[i]==':') {
      continue;
    }

    if (pos>sizeof(clientId)-2) {
      break;
    }

    clientId[pos] = (char)mac[i];
    pos++;
  }  

  clientId[pos]=0;
  Serial.print("ClientId: ");
  Serial.println(clientId);
}
