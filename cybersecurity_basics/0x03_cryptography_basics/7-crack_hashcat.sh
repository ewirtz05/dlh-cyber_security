#!/bin/bash
hashcat -a 0 -m 0 "$1" /usr/share/wordlists/rockyou.txt --outfile 7-password.txt --outfile-format=2 || true
hashcat -a 3 -m 0 "$1" ?l?l?l?l?l?l --outfile 7-password.txt --outfile-format=2
