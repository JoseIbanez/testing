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
//#include <Wire.h>
//#include <Adafruit_BME280.h>
//#include <Adafruit_Sensor.h>



// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.1.144";
//const char* mqtt_server = "YOUR_MQTT_BROKER_IP_ADDRESS";
#define MQTT_SERVER      "192.168.1.19"
#define MQTT_PORT        1883
#define MQTT_CLIENT_ID   "ESP"
#define MQTT_TOPIC_OUT   "output"
#define MQTT_TOPIC_TEMP  "temperature"
#define MQTT_TOPIC_HUMI  "humidity"

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
long lastBoot = 0;
char msg[50];
int value = 0;
String mac;
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

// LED Pin
const int ledPin = 1;


void wifi_setup() {
  delay(100);
  int count = 0;
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    count++;
    if (count>30) {
      Serial.println("");
      Serial.println("WiFi setup failed");
      return;
    }
  }

  Serial.println("");
  Serial.println("WiFi connected");

	mac = WiFi.macAddress();
  Serial.print("WiFi MAC: ");
	Serial.println(mac);

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}


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
      digitalWrite(ledPin, HIGH);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      digitalWrite(ledPin, LOW);
    }
  }
}

void set_clientId() {

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

void reconnect() {

  Serial.print("Attempting MQTT connection...");
  // Attempt to connect
  if (client.connect(clientId)) {
    Serial.println("connected");
    // Subscribe
    client.subscribe(MQTT_TOPIC_OUT);
  } else {
    Serial.print("failed, rc=");
    Serial.print(client.state());
    Serial.println(" try again in 1 seconds");
    delay(1000);
  }

}



void setup() {
  Serial.begin(9600);
  
  lastBoot = millis();
  sleep_setup();
  
  wifi_setup();

  set_clientId();

  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);

  pinMode(ledPin, OUTPUT);
}


void loop() {

  long now = millis();

  if (now - lastBoot > 30000 || WiFi.status() != WL_CONNECTED) {
    client.disconnect();
    sleep_now();
  }

  if (!client.connected()) {
    reconnect();
  }

  if (!client.connected()) {
    sleep(1);
    return;
  }

  client.loop();


  if (now - lastMsg > 5000) {
    lastMsg = now;
    char topic[50];
    
    // Temperature in Celsius
    // temperature = bme.readTemperature();   
    // Uncomment the next line to set temperature in Fahrenheit 
    // (and comment the previous temperature line)
    //temperature = 1.8 * bme.readTemperature() + 32; // Temperature in Fahrenheit
    temperature = 21;

    // Convert the value to a char array
    char tempString[8];
    dtostrf(temperature, 1, 2, tempString);
    Serial.print("Temperature: ");
    Serial.println(tempString);
    strcpy(topic,clientId);
    strcat(topic,"/");
    strcat(topic,MQTT_TOPIC_TEMP);
    client.publish(topic, tempString);

    //humidity = bme.readHumidity();
    humidity = 50;

    // Convert the value to a char array
    char humString[8];
    dtostrf(humidity, 1, 2, humString);
    Serial.print("Humidity: ");
    Serial.println(humString);
    strcpy(topic,clientId);
    strcat(topic,"/");
    strcat(topic,MQTT_TOPIC_HUMI);
    client.publish(topic, humString);
  }
}