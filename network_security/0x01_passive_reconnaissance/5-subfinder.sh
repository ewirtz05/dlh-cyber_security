#!/bin/bash
subfinder -d "$1" -silent | while read sub; do ip=$(dig +short "$sub" A | head -n 1); [ -n "$ip" ] && echo "$sub,$ip"; done > "${1%%.*}.txt"
