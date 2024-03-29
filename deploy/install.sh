#!/bin/bash

#-----------------------------
version=$(cat VERSION)
echo 'Installing Phew ('${version}')...'

echo 'Building docker image...'
cd ..
cp ./deploy/Dockerfile ./
docker build --build-arg VER=${version} -f ./Dockerfile -t phew:${version} .
rm Dockerfile
cd ./deploy

#make dir for data
if [ ! -d "/data" ]; then
	mkdir /data
fi
if [ ! -d "/data/phewdata" ]; then
	echo 'Making path (/data/phewdata) for cache...'
	mkdir /data/phewdata
fi

echo 'starting Phew service...'
#start container
docker run \
--name phew \
--network=host \
-v /data/phewdata:/phewdata \
-v /data/yn/dzjz/:/juanzong \
--restart=always \
-d phew:${version} \
bash startphew.sh

echo 'Phew service started'
