#!/bin/bash
sudo find "$1" -type f -exec chmod o-w {} \;
