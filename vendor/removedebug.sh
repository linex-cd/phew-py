#!/bin/bash

version=$(cat VERSION)

docker stop textise_vendor_debug
docker rm textise_vendor_debug

docker rmi textise_vendor:${version}

