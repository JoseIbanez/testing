#!/bin/bash


curl http://127.0.0.1:43110/13aNmBWAkWzaXT1Hva4B9kpJW1nWFjFF4X/Lista%20acestream.m3u  > ./listas/ramses.latin.m3u8
curl http://127.0.0.1:43110/electroperra.list/channels.txt > ./listas/electroperra.latin.m3u8  

iconv -f iso-8859-1 -t utf-8 ./listas/ramses.latin.m3u8 > ./listas/ramses.m3u8
iconv -f iso-8859-1 -t utf-8 ./listas/electroperra.latin.m3u8 > ./listas/electroperra.m3u8


#curl https://raw.githubusercontent.com/grupolecturyamigos/grupolectura/main/Lecturas.m3u > ./listas/lecturas.m3u8

