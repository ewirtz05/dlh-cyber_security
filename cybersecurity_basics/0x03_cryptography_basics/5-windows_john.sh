#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=NT "$1" && john --show --format=NT "$1" | grep -v "password hash" | cut -d: -f2 > 5-password.txt
