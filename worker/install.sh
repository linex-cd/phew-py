#!/bin/bash

#-----------------------------
version=$(cat VERSION)


#-----------------------------

#image
docker build -f ./Dockerfile -t textise_service:${version} .

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

container_name=textise_worker_node_${i}

WORKER_ID=${i}
WORKER_NAME=Nanjing-Dev-worker-node-${i}
WORKER_LOCATION=南京

nvidia-docker run \
--name ${container_name} \
-v /data/yn/dzjz/:/juanzong \
--network=host \
-e WORKER_ID=${WORKER_ID} \
-e WORKER_NAME=${WORKER_NAME} \
-e WORKER_LOCATION=${WORKER_LOCATION} \
--restart=always \
-d textise_service:${version} \
bash startworker.sh

done
