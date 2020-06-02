#!/bin/bash

#-----------------------------
version=$(cat VERSION)

#image
docker build -f ./Dockerfile -t textise_system:${version} .

#debug
nvidia-docker run \
--name jobcenter_debug \
--network=host \
-v /data/tmdata:/tmdata \
-v /data/yn/dzjz/:/file \
-it textise_system:${version} \
bash