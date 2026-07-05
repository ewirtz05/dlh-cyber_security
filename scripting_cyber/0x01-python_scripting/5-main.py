#!/usr/bin/env python3

check_port = __import__("5-port_scanner").check_port

print(check_port("scanme.nmap.org", 80))
print(check_port("scanme.nmap.org", 9999))
