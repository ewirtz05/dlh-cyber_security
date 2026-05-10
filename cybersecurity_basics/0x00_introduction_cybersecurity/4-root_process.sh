#!/bin/bash
ps -u "$1" -o user,%cpu,%mem,vsz,rss,tty,stat,start,time,command | grep -v " 0 0 "
