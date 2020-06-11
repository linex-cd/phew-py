#!/bin/bash

#-----------------------------
version=$(cat VERSION)

#config
ENABLE_STATISTIC=yes

#database
KAFKA_SERVER=192.168.2.31
DB=postgresql://postgres:postgres@192.168.2.31:5432/cv

#aliyun oss
OSS_ACCESS_KEY_ID=xxx
OSS_ACCESS_KEY_SECRET=xxx
OSS_BUCKET=xxx
OSS_ENDPOINT=xxx
#-----------------------------

#image
docker build -f ./Dockerfile -t textise_vendor:${version} .

#vendor service
node_id=1

if [ -n "$1" ]; then
    node_id=$1
else
    echo "第一个参数是节点ID，默认1"
fi

INSTANT_ID=textise_vendor_node_${node_id}
container_name=textise_vendor_${node_id}

nvidia-docker run \
--name=${container_name} \
--network=host \
-v /data/yn/dzjz/:/juanzong \
-v /data/dockerdata/ocr:/data \
-e INSTANT_ID=${INSTANT_ID} \
-e KAFKA_SERVER=${KAFKA_SERVER} \
-e DB=${DB} \
-e OSS_ACCESS_KEY_ID=${OSS_ACCESS_KEY_ID} \
-e OSS_ACCESS_KEY_SECRET=${OSS_ACCESS_KEY_SECRET} \
-e OSS_BUCKET=${OSS_BUCKET} \
-e OSS_ENDPOINT=${OSS_ENDPOINT} \
--restart=always \
-d textise_vendor:${version} \
bash startvendor.sh

