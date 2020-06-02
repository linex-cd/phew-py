#!/bin/bash

version=$(cat VERSION)

echo "removing jobcenter_debug service..."
docker stop jobcenter_debug &&  docker rm jobcenter_debug
