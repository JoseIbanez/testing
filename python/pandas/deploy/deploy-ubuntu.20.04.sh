#!/bin/bash

#Ubuntu 20.04
apt update -y
apt install -y default-jre python3-pip

snap install luigi-server
snap install google-cloud-sdk --classic

pip3 install -r requirements.txt




mkdir -p $HOME/.secrets/
mkdir -p /etc/luigi
cp ./luigi.cfg /etc/luigi/

PATH=$PATH:/home/vagrant/.local/bin
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.secrets/ibanez-001-8e1126c08504.json"





url="https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Actualizacion_123_COVID-19.pdf"

