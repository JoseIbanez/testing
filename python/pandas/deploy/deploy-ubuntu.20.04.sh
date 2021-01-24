#!/bin/bash

#Ubuntu 20.04
sudo apt update -y
sudo apt install -y default-jre python3-pip

sudo snap install google-cloud-sdk --classic

pip3 install -r requirements.txt




#mkdir -p /etc/luigi
#cp ./luigi.cfg /etc/luigi/
PATH=$PATH:/home/vagrant/.local/bin





url="https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Actualizacion_123_COVID-19.pdf"

