#!/usr/bin/env python3

crawl_website = __import__("4-web_crawler").crawl_website

urls = crawl_website("https://google.com", max_depth=2)

for url in sorted(urls):
	print(url)
