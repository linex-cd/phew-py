#!/bin/bash

version=$(cat VERSION)


node_count=5
start_node=0

if [ -n "$1" ]; then
    node_count=$1
else
    echo "第一参数是部署节点数，默认5"
fi

if [ -n "$2" ]; then
    start_node=$2
else
    echo "第二参数是部署的起始节点数，默认0"
fi


for i in `seq ${node_count}`
do

let i=`expr ${i}+${start_node}`

docker stop textise_worker_node_${i}
docker rm textise_worker_node_${i}

done

docker rmi textise_service:${version}