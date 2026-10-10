#!/bin/bash
nmap -A -sV -sC --script banner,ssl-enum-ciphers,smb-enum-domains --traceroute -oN service_enumeration_results.txt $1
