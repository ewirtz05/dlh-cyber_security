#!/usr/bin/env python3

get_http_headers = __import__("3-http_headers").get_http_headers

result = get_http_headers("http://www.google.com")

if result:
	print(result["status_code"])
	print(result["headers"])
else:
	print("Request failed")
