#!/bin/bash

version=$(cat VERSION)

port=8001

if [ -n "$1" ]; then
    port=$1
else
    echo "第一个参数是服务端口，默认8001"
fi

docker stop textise_web_${port} &&  docker rm textise_web_${port}


docker rmi textise_web:${version}