#!/usr/bin/env python3
"""
Basic Reconnaissance
Combines DNS Lookup, web reconnaissance, simple TCP port checking
"""

import socket
import subprocess
import requests
from bs4 import BeautifulSoup

# import dns

def dns_recon(domain):
	"""Resolve domain IP adress and retrieve MX records"""
	print("=== DNS Reconnaissance ===")

	try:
		ip = socket.gethostbyname(domain)
		print(f"IP Address: {ip}")
	except socket.gaierror:
		print("IP Address: Could not resolve domain")

	print("MX Records:")
	try:
		result = subprocess.run(
			["nslookup", "-type=MX", domain],
			capture_output=True,
			text=True,
			timeout=5
		)

		found = False
		for line in result.stdout.splitlines():
			if "mail exchanger" in line.lower() or "mx preference" in line.lower():
				print(line.strip())
				found = True

		if not found:
			print("No MX records found")

	except Exception:
		print("Could not retrieve MX records")

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
		print(f"Web request failed: {error}")

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

def main():
	"""Run the full reconnaissance script"""
	domain = input().strip()

	print("NETWORK RECONNAISSANCE TOOL")
	print("===========================")
	print(f"Target: {domain}")
	print()

	dns_recon(domain)
	web_recon(domain)
	port_scan(domain)

if __name__ == "__main__":
	main()
