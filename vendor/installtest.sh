#!/bin/bash

#-----------------------------
version=$(cat VERSION)

#database
KAFKA_SERVER=192.168.2.31
DB=postgresql://postgres:postgres@192.168.2.31:5432/cv

#aliyun oss
OSS_ACCESS_KEY_ID=LTAI4Fpv3g2wjPFnKwAp4a4S
OSS_ACCESS_KEY_SECRET=EpO8bWdrq2DjAeLX90y5aTX6Gp5js3
OSS_BUCKET=znfz
OSS_ENDPOINT=http://oss-cn-hangzhou.aliyuncs.com

#-----------------------------
#image
docker build -f ./Dockerfile -t textise_vendor:${version} .

#-----------------------------
#config
WORKER_GROUP=Nanjing
WORKER_KEY=testkey12345
WORKER_ROLE=textise

node_id=1

if [ -n "$1" ]; then
    node_id=$1
else
    echo "第一个参数是节点ID，默认1"
fi

INSTANT_ID=textise_vendor_node_${node_id}
container_name=textise_vendor_${node_id}

VENDOR_ID=${node_id}
VENDOR_NAME=Nanjing-Dev-vendor-node-${node_id}
VENDOR_LOCATION=南京

nvidia-docker run \
--name=${container_name} \
--network=host \
-v /data/yn/dzjz/:/juanzong \
-v /data/yn/kafka-files/:/kafkacache \
-v /data/dockerdata/ocr:/data \
-e VENDOR_ID=${VENDOR_ID} \
-e VENDOR_NAME=${VENDOR_NAME} \
-e VENDOR_LOCATION=${VENDOR_LOCATION} \
-e WORKER_GROUP=${WORKER_GROUP} \
-e WORKER_KEY=${WORKER_KEY} \
-e WORKER_ROLE=${WORKER_ROLE} \
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

