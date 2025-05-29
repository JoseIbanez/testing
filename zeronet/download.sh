#!/bin/bash

curl http://127.0.0.1:43110/12Yeki2J1iXKurXSqL5JupkBjp1P4eYuEw/Icastresana.m3u    > ./listas/elcano.m3u8
curl http://127.0.0.1:43110/1DfXfvZdWCkNKYmQkD6ezBL2Q9V32vZnhx/lista1.m3u         > ./listas/pmeister.m3u8
curl http://127.0.0.1:43110/13aNmBWAkWzaXT1Hva4B9kpJW1nWFjFF4X/Lista%20acestream.m3u  > ./listas/ramses.m3u8

#curl http://127.0.0.1:43110/electroperra.list/channels.txt > ./listas/electroperra.origin.m3u8  




#encoding=$(file -b --mime-encoding myfile.txt)

#iconv -f iso-8859-1 -t utf-8 ./listas/electroperra.origin.m3u8 > ./listas/electroperra.m3u8




#curl https://raw.githubusercontent.com/grupolecturyamigos/grupolectura/main/Lecturas.m3u > ./listas/lecturas.m3u8

