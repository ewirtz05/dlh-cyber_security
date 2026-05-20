#!/bin/bash
find "$1" -type f -user user2 -exec sudo chown user3 {} \;
