#!/bin/bash
sudo nmap -sX --open --packet-trace --reason -p 440,450 $1
