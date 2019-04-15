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

//Geekworm board
//#define LED_BUILTIN 0

#define DEBUG 1

WiFiClient espClient;
PubSubClient client(espClient);
long lastBeacon = 0;
long lastBoot = 0;
long lastOrder = 0;

char msg[50];
int value = 0;
char clientId[20];
String relayStatus;
int curTime;


// Parse cmd
int parse_cmd(String input) {

  char delimiter[] = ";";
  char* ptr;
  char buf[15];

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
    lastOrder = millis();
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



// callback function
void callback(char* topic, byte* message, unsigned int length) {
  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageOrder;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageOrder += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  //if (String(topic) == MQTT_TOPIC_OUT) {
  parse_cmd(messageOrder);
  update_gpio(relayStatus);
  //}

  char aTopic[50];    
  strcpy(aTopic,"a/");
  strcat(aTopic,clientId);
  client.publish(aTopic, "ok");

  delay(100);
  digitalWrite(LED_BUILTIN, HIGH);
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
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  lastBoot = millis();
  sleep_setup();
  setup_wifi();  
  set_clientId(clientId,sizeof(clientId));
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
  digitalWrite(LED_BUILTIN, HIGH);
}


void loop() {

  long now = millis();

  if (WiFi.status() != WL_CONNECTED) {
    sleep_now();
  }

  if (!client.connected()) {
    if(reconnect() < 0) {
      delay(1000);
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

  if (curTime > 0) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    //Serial.println(".");
  }

  if ( curTime > 0   &&   (now - lastOrder) > curTime*1000 ) {
    curTime = 0;
    relayStatus = "0000";
    update_gpio(relayStatus);
  }

}