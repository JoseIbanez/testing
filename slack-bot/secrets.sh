#!/bin/bash

gpg -o var.env.gpg --symmetric --passphrase-file ~/.ssh/personal.pass var.env

