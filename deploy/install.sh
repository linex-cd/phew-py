#!/bin/bash

#-----------------------------

version=$(cat VERSION)
echo 'Installing Job Center ('+${version}+')...'

echo 'Building docker image...'
#image
docker build --build-arg version=${version} -f ./Dockerfile -t jobcenter:${version} .

#make dir for data
if [ ! -d "/data" ]; then
	mkdir /data
fi
if [ ! -d "/data/jobcenterdata" ]; then
	echo 'Making path (/data/jobcenterdata) for cache...'
	mkdir /data/jobcenterdata
fi


echo 'starting Job Center service...'
#start container
docker run \
--name jobcenter \
--network=host \
-v /data/jobcenterdata:/jobcenterdata \
--restart=always \
-d jobcenter:${version} \
bash startkjobcenter.sh

echo 'Job Center service started'
