#!/bin/bash

version=$(cat ../VERSION)

#save image
docker save -o jobcenter_image_${version}.tar jobcenter_image:${version}