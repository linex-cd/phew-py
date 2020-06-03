#!/bin/bash

#-----------------------------
version=$(cat VERSION)
echo 'Installing Job Center ('${version}')...'

echo 'Building docker image...'
cd ..
cp ./deploy/Dockerfile ./
docker build --build-arg VER=1.0.0 -f ./Dockerfile -t jobcenter:${version} .
rm Dockerfile
cd ./deploy

#make dir for data
if [ ! -d "/data" ]; then
	mkdir /data
fi
if [ ! -d "/data/jobcenterdata" ]; then
	echo 'Making path (/data/jobcenterdata) for cache...'
	mkdir /data/jobcenterdata
fi

echo 'starting Job Center Debug mode...'
#start container
docker run \
--name jobcenter_debug \
--network=host \
-v /data/jobcenterdata:/jobcenterdata \
-it jobcenter:${version} \
bash

