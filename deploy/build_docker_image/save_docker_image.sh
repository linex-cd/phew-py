#!/bin/bash

version=$(cat ../VERSION)

#save image
docker save -o jobcenter_image_${version}.tar