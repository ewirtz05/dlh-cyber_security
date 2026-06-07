# 0x0B Web Security

This directory contains solutions for the Web Security tasks.

## Task 0 - User Enumeration

The objective was to identify a valid username through the `/api/check_username` endpoint.

The endpoint accepts POST requests with JSON data:

```bash
curl -k -X POST \
-H "Content-Type: application/json" \
-d '{"username":"admin"}' \
"https://web-80-76-242.cod-eu-west-3.hbtn.io/api/check_username"
