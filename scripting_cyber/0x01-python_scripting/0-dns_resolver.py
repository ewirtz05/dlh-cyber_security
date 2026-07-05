#!/usr/bin/env python3

import socket

def resolve_domain_to_ip4(domain_name):
	"""
	Resolve a domain name to its IPv4 address
	
	Args:
		domain_name (str)
	
	Returns:
		str: IPv4 if resolved successfully
		None: If the domain cannot be resolved
		str: Error message for exceptions
	"""
	try:
		return socket.gethostbyname(domain_name)
	except socket.gaierror:
		return None
	except Exception as error:
		return str(error)

if __name__ == "__main__":
	pass
