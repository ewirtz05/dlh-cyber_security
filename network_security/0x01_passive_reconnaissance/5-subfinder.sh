#!/bin/bash
subfinder -d "$1" -silent | while read subdomain; do ip=$(host "$subdomain" | grep "has address" | head -n 1 | awk '{print $4}'); [ -n "$ip" ] && echo "$subdomain, $ip"; done > domain.txt
