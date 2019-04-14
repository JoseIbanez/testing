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
#include "gpio.h"


WiFiClient espClient;
PubSubClient client(espClient);
long lastBeacon = 0;
long lastBoot = 0;
char msg[50];
int value = 0;
char clientId[20];
int curTime;
String relayStatus;


// callback function
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


///////
int parse_cmd(String input) {

  char delimiter[] = ";";
  char* ptr;
  char buf[4];

  #ifdef DEBUG
  Serial.println(input);
  #endif

  //Asking for status ?
  if ((input == "STATUS") || (input == "S")) {
    return 0;
  }
  
  
  input.toCharArray(buf, sizeof(buf));

  // Get TimeOut
  ptr = strtok(buf, delimiter);
  if (ptr != NULL) {
    curTime = String(ptr).toInt();
    Serial.println("Uptime: " + String(curTime));
  }

  // Get Gpio Status
  ptr = strtok (NULL, delimiter);
  if (ptr != NULL) {
    relayStatus = String(ptr);
    Serial.println("Relay status: " + relayStatus);
  }

  // Sanity
  if (curTime <= 0) {
    curTime = 0;
    relayStatus = "0000";
  }

  return(0);
}


////////
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