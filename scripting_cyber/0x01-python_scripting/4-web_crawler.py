#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_website(start_url, max_depth=2):
	"""
	Recursively crawl a website and return visited internal URLs

	Args:
		start_url (str): URL to start crawling from
		max_depth (int): Maximum crawl depth

	Returns:
		set: URLs successfully visited.
	"""
	visited = set()

	try:
		start_domain = urlparse(start_url).netloc
		if not start_domain:
			return set()
	except Exception:
		return set()

	def crawl(url, depth):
		if depth > max_depth or url in visited:
			return

		try:
			parsed_url = urlparse(url)

			if parsed_url.netloc != start_domain:
				return

			response = requests.get(url, timeout=5)
			response.raise_for_status()

			visited.add(url)

			soup = BeautifulSoup(response.text, "html.parser")

			for link in soup.find_all("a", href=True):
				href = link.get("href")
				absolute_url = urljoin(url, href)

				parsed_link = urlparse(absolute_url)

				if parsed_link.scheme not in ("http", "https"):
					continue

				if parsed_link.netloc == start_domain:
					crawl(absolute_url, depth + 1)

		except requests.exceptions.RequestException:
			return
		except Exception:
			return

	crawl(start_url, 0)
	return visited
