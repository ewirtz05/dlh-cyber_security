#!/bin/bash
password="$1"
salt=$(openssl rand -hex 8)
echo -n "${password}${salt}" | openssl dgst -sha512 > 3_hash.txt
