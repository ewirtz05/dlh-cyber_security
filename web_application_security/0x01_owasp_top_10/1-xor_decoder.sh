#!/bin/bash

hash="$1"
encoded="${hash#\{xor\}}"

echo "$encoded" | base64 -d | python3 -c '
import sys

data = sys.stdin.buffer.read()
decoded = bytes(byte ^0x5f for byte in data)
sys.stdout.buffer.write(decoded)
'

echo
