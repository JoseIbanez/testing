#!/bin/bash


jfrog rt u "(*).tgz" generic-local/{1}/ --recursive=false


jfrog rt u --recursive=true --flat=false ./ vrealize-build-tools

jfrog rt u --recursive=true --flat=false ./ vro-local




