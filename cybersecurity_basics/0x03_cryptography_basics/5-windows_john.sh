#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=NT "$1" >/dev/null 2>&1; john --show --format=NT "$1" | awk -F: '/:/ {print $2; exit}' > 5-password.txt
