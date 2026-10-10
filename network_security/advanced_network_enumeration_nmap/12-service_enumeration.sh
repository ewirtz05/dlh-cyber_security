#!/bin/bash
nmap -A -sV --script banner,ssl-enum-ciphers,smb-enum-domains,default --traceroute -oN service_enumeration_results.txt $1
