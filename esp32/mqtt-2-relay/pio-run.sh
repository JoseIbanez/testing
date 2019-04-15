#!/bin/bash

ENV=Geekworm
ENV=lolin32

sudo chown vagrant /dev/ttyUSB0 
platformio run -e $ENV -t upload -t monitor

