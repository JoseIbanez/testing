#!/bin/bash
microk8s enable helm3
microk8s.helm3 list

alias helm='microk8s.helm3'
