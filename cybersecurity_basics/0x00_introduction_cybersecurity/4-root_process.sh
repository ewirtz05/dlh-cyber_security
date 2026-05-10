#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 <username>"
    exit 1
fi
USER_NAME=$1
ps -u "$USER_NAME" -o user,%cpu,%mem,vsz,rss,tty,stat,start,time,command | grep -v " 0 0 "
