#!/bin/bash
sudo nmap -Pn --script ssl-enum-ciphers -p 443 "$1"
