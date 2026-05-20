#!/bin/bash
find "$1" -user user2 -exec sudo chown user3 {} \;
