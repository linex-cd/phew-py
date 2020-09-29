#!/bin/bash

#-----------------------------
version=$(cat VERSION)


#database
KAFKA_SERVER=127.0.0.1
DB=postgresql://postgres:1234@127.0.0.1:5432/cv

#aliyun oss
OSS_ACCESS_KEY_ID=xxxx
OSS_ACCESS_KEY_SECRET=xxxx
OSS_BUCKET=znfz
OSS_ENDPOINT=xxxx

#-----------------------------
#image

#-----------------------------
#config
WORKER_GROUP=Hangzhou
WORKER_KEY=testkey12345
WORKER_ROLE=textise


INSTANT_ID=textise_vendor_node_debug
container_name=textise_vendor_debug

VENDOR_ID=${node_id}
VENDOR_NAME=Hangzhou-Prod-vendor-node-debug
VENDOR_LOCATION=杭州

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
-it textise_vendor:${version} \
bash

