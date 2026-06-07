#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt "$1" --format=Raw-MD5 && john --show "$1" --format=Raw-MD5 | grep ":" | cut -d: -f2 > 4-password.txt
