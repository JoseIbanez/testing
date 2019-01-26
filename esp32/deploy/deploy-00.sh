#!/bin/bash

sudo apt-get update -y 
sudo apt-get install -y git wget make libncurses-dev flex bison gperf python python-serial
sudo apt-get install -y python-pip


wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-73-ge28a011-5.2.0.tar.gz

mkdir esp
cd esp
tar -xzf ../xtensa-esp32-elf-linux64-1.22.0-73-ge28a011-5.2.0.tar.gz 
alias get_esp32='export PATH="$PATH:$HOME/esp/xtensa-esp32-elf/bin"'
get_esp32

git clone --recursive https://github.com/espressif/esp-idf.git

export IDF_PATH=~/esp/esp-idf


cp -r $IDF_PATH/examples/get-started/hello_world .

/usr/bin/python -m pip install --user -r /home/vagrant/esp/esp-idf/requirements.txt


sudo chown vagrant /dev/ttyUSB0
alias get_esp32='export PATH="$PATH:$HOME/esp/xtensa-esp32-elf/bin"'
get_esp32
export IDF_PATH=~/esp/esp-idf


#to exit:
#--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---

