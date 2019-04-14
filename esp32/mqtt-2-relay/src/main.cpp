/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com

  Read Mac:  
    https://www.arduino.cc/en/Reference/WiFiMACAddress
*********/

#include <WiFi.h>
#include <PubSubClient.h>
#include "secrets.h"
#include "sleep.h"
#include "setup.h"
#include "config.h"
//#include <Wire.h>
//#include <Adafruit_BME280.h>
//#include <Adafruit_Sensor.h>



WiFiClient espClient;
PubSubClient client(espClient);
long lastBeacon = 0;
long lastBoot = 0;
char msg[50];
int value = 0;
char clientId[20];

//uncomment the following lines if you're using SPI
/*#include <SPI.h>
#define BME_SCK 18
#define BME_MISO 19
#define BME_MOSI 23
#define BME_CS 5*/

//Adafruit_BME280 bme; // I2C
//Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI
float temperature = 0;
float humidity = 0;
float moisture = 0;


// LED Pin
//const int ledPin = 1;




void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  if (String(topic) == MQTT_TOPIC_OUT) {
    Serial.print("Changing output to ");
    if(messageTemp == "on"){
      Serial.println("on");
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}




int reconnect() {
  char topic[50];

  Serial.print("Attempting MQTT connection...");
  // Attempt to connect
  if (!client.connect(clientId)) {
    Serial.print("failed, rc=");
    Serial.print(client.state());
    Serial.println(" try again in 1 seconds");
    delay(1000);
    return -1;
  }
  Serial.println("Connected.");
  
  // Subscribe
  strcpy(topic,"q/");
  strcat(topic,clientId);
  client.subscribe(topic);
  Serial.print("Suscribed to topic=");
  Serial.println(topic);

  return 0;
}



void setup() {
  Serial.begin(9600);
  lastBoot = millis();
  sleep_setup();  
  setup_wifi();
  set_clientId(clientId);
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
  pinMode(LED_BUILTIN, OUTPUT);
}


void loop() {

  long now = millis();

  if (WiFi.status() != WL_CONNECTED) {
    sleep_now();
  }

  if (!client.connected()) {
    if(reconnect() < 0) {
      sleep(1);
      return;
    } 
  }

  client.loop();

  // Send beacon message
  if (now - lastBeacon > 60000) {
    lastBeacon = now;
    char topic[50];    
    strcpy(topic,"b/");
    strcat(topic,clientId);
    client.publish(topic, "");
  }


}