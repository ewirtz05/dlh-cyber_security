#!/bin/bash
subfinder -d "$1" -silent | while read subdomain; do host "$subdomain" | grep "has address" | awk -v sub="$subdomain" '{print sub", "$4}'; done > "$1.txt"
