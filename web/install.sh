#!/bin/bash

#-----------------------------
version=$(cat VERSION)

#image
docker build -f ./Dockerfile -t textise_web:${version} .

port=8001

if [ -n "$1" ]; then
    port=$1
else
    echo "第一个参数是服务端口，默认8001"
fi

#web service
nvidia-docker run \
--name textise_web_${port} \
--network=host \
--restart=always \
-e SERVER_PORT=${port} \
-d textise_web:${version} \
bash startweb.sh

