#!/bin/bash

version=$(cat VERSION)

echo "Removing Job Center service..."
docker stop jobcenter &&  docker rm jobcenter

echo "Removing docker image..."
docker rmi jobcenter:${version}

