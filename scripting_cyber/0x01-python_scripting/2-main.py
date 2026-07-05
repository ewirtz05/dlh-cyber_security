#!/usr/bin/env python3

download_page = __import__("2-download_page").download_page

html = download_page("http://example.com")
print(html)
