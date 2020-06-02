#!/bin/bash

version=$(cat VERSION)

echo "removing jobcenterservice..."
docker stop jobcenter &&  docker rm jobcenter

echo "removing system image..."
docker rmi textise_system:${version}

