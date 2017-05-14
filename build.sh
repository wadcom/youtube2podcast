#! /bin/sh -e

if [ $# -eq 0 ]; then
    TAG=latest
elif [ $# -eq 1 ]; then
    TAG=$1
else
    echo "Usage: $0 [TAG]" >&2
    exit 1
fi

docker build -t wadcom/youtube2podcast:$TAG .
