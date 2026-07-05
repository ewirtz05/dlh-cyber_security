#!/usr/bin/env python3

import socket

def check_port(host, port):
	"""Return True for open port, otherwise False"""
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)

		result = sock.connect_ex((host, port))
		sock.close()

		return result == 0

	except Exception:
		return False
