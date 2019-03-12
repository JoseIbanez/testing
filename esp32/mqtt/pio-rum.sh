#!/bin/bash

sudo chown vagrant /dev/ttyUSB0 
platformio run -t upload -t monitor

