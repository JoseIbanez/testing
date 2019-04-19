#!/bin/bash

#Setup VM OS

sudo apt-get -y update
sudo apt-get -y install python-pip
sudo apt-get -y install linux-image-extra-virtual

sudo chown vagrant /dev/ttyUSB0 


# pio install 
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


#Compile and load
platformio run -t upload -t monitor


#udev rules
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/scripts/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
