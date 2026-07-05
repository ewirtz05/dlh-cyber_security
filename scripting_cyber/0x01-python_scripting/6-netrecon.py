#!/usr/bin/env python3
"""
Basic Reconnaissance
Combines DNS Lookup, web reconnaissance, simple TCP port checking
"""

import socket
import requests
from bs4 import BeautifulSoup
import dns.resolver

def dns_recon(domain):
	"""Resolve domain IP adress and retrieve MX records"""
	print("=== DNS Reconnaissance ===")

	try:
		ip_address = socket.gethostbyname(domain)
		print(f"IP Address: {ip_address}")
	except socket.gaierror:
		print("IP Address: Could not resolve domain")

	try:
		mx_records = dns.resolver.resolve(domain, "MX")
		print ("MX Records:")
		for record in mx_records:
			print(f" {record.exchange} priority {record.preference}")
	except Exception:
		print("MX Records: Could not retrieve")

	print()

def web_recon(domain):
	"""Send HTTP request, display status code, selected headers, link count"""
	print("=== Web Reconnaissance ===")

	url = f"http://{domain}"

	try:
		response = requests.get(url, timeout=5)

		print(f"HTTP Status Code: {response.status_code}")

		print("Selected Headers:")
		selected_headers = ["Server", "Content-Type", "Content-Length"]
		for header in selected_headers:
			value = response.headers.get(header)
			if value:
				print(f" {header}: {value}")

		soup = BeautifulSoup(response.text, "html.parser")
		links = soup.find_all("a")
		print(f"Number of Links: {len(links)}")

	except requests.exceptions.RequestException as error:
		print("Web request failed: {error}")

	print()

def port_scan(domain):
	""" Check common TCP ports"""
	print("=== Port Checking ===")

	common_ports = [21, 22, 25, 53, 80, 110, 143, 443]

	try:
		ip_address = socket.gethostbyname(domain)
	except socket.gaierror:
		print("Could not resolve domain for port scanning")
		print()
		return

	print(f"Scanning host: {ip_address}")

	for port in common_ports:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(1)

			result = sock.connect_ex((ip_address, port))

			if result == 0:
				print(f"Port {port}: Open")

			sock.close()

		except socket.error:
			pass

	print()

if __name__ == "__main__":
	target_domain = "google.com"

	print(f"Reconnaissance Report for {target_domain}")
	print("=" * 40)
	print()

	dns_recon(target_domain)
	web_recon(target_domain)
	port_scan(target_domain)
