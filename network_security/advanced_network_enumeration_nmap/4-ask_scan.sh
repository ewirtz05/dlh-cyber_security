#!/bin/bash
sudo nmap -sA -p $2 --reason --max-rtt-timeout 1000ms  $1
