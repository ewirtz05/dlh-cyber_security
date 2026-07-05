#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def download_page(url):
	"""
	Donwload a webpage and return formatted HTML content

	Args:
		url (str): The URL of the webpage

	Returns:
		str: HTML if successful, otherwise error
	"""
	try:
		response = requests.get(url)
		response.raise_for_status()

		soup = BeautifulSoup(response.text, "html.parser")
		return soup.prettify()

	except requests.exceptions.RequestException as e:
		return f"Error downloading page: {e}"
