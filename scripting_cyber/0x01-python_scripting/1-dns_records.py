#!/usr/bin/env python3

import sys
import dns.resolver

def query_dns_records(domain_name):
	"""
	Query DNS records for A, AAAA, MX, NS, TXT, SOA

	Args:
		domain_name (str): Domain name

	Returns:
		dict: DNS answers by type
	"""
	record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA"]
	results = {}

	for record_type in record_types:
		try:
			answers = dns.resolver.resolve(domain_name, record_type)
			results[record_type] = answers

		except (
			dns.resolver.NoAnswer,
			dns.resolver.NXDOMAIN,
			dns.resolver.NoNameservers,
		):
			pass

	return results

if __name__ == "__main__":
	domain_name = sys.argv[1]
	results = query_dns_records(domain_name)

	for record_type, response_text in results.items():
		print(f"\n{record_type} Records:")
		print(response_text.response.to_text())
	print("\nResults dictionary:", results)
