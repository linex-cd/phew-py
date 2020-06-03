#!/bin/bash

version=$(cat VERSION)

echo "Removing Job Center Debug service..."
docker stop jobcenter_debug &&  docker rm jobcenter_debug
