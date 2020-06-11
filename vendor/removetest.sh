#!/bin/bash

version=$(cat VERSION)

node_id=1

if [ -n "$1" ]; then
    node_id=$1
else
    echo "第一个参数是节点ID，默认1"
fi

docker stop textise_vendor_${node_id}
docker rm textise_vendor_${node_id}

docker rmi textise_vendor:${version}