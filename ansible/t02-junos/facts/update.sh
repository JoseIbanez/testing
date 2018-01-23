#!/bin/bash

sudo cp facts/* /etc/ansible/facts.d/
sudo chmod 666 /etc/ansible/facts.d/*
ansible localhost -m setup -a "filter=ansible_local"

