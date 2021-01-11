#!/bin/bash

echo 如果出现无法解析DNS，修改/etc/default/docker文件，取消注释：DOCKER_OPTS="–dns 8.8.8.8 –dns 8.8.4.4"


#pull base image
docker pull python:3.6

#-----------------------------
version=$(cat ./VERSION)

#build image
docker build -f ./BuildImageDockerfile -t phew_image:${version} .

