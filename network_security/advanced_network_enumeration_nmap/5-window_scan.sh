#!/bin/bash
sudo nmap -sW -p $2 -p- $3 $1
