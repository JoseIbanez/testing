#!/bin/bash

apt install -y default-jre
apt install -y python3.7-minimal python3-pip
python3.7 -m pip install pip
python3.7 -m pip install tabula-py
python3.7 -m pip install luigi
python3.7 -m pip install pdfminer.six



PATH=$PATH:/home/vagrant/.local/bin


url="https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Actualizacion_123_COVID-19.pdf"

