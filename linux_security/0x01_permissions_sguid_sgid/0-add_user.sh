#!/bin/bash
# Create a new user and set its password
sudo useradd -m "$1" && echo "$1:$2" | sudo chpasswd
