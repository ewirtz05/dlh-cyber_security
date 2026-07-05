#!/usr/bin/env python3

import requests

def get_http_headers(url):
	"""
	Retrieve HTTP response headers from a website

	Args:
		url (str): website URL

	Returns:
		dict: Dictionary with status_code and headers when successful
		None: if request fails
	"""
	try:
		response = requests.get(url)
		return {
			"status_code": response.status_code,
			"headers": dict(response.headers)
		}
	except requests.exceptions.RequestException:
		return None
