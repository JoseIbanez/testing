#ifndef H_CONFIG
#define H_CONFIG


// Add your MQTT Broker IP address, example:
#define MQTT_SERVER      "192.168.1.19"
#define MQTT_PORT        1883
#define MQTT_CLIENT_ID   "ESP"
#define MQTT_TOPIC_OUT   "output"
#define MQTT_TOPIC_TEMP  "temp"
#define MQTT_TOPIC_HUMI  "humi"
#define MQTT_TOPIC_MOIS  "mois"

#define DEBUG 1

//#define MQTT_TOPIC_CALLHOME  "callhome"

//Geekworm board
//#define LED_BUILTIN 0

//relay ports
#define RELAY1 25
#define RELAY2 26
#define RELAY3 27
#define RELAY4 14


#endif