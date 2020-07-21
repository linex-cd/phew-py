#!/bin/bash

version=$(cat ../VERSION)

#load
docker load -i jobcenter_image_${version}.tar
