#!/bin/bash

pip install -U platformio


platformio platform install atmelavr
platformio platform install espressif32

platformio lib install 

#myBoards

#Geekworm EASY KIT ESP32 C1
http://www.raspberrypiwiki.com/index.php/ESP32-DevKit

#AZDelivery NodeMCU32
https://www.az-delivery.de/collections/wifi-module/products/esp32-developmentboard?ls=en


#Project init
platformio init --board esp32dev 
platformio lib list




