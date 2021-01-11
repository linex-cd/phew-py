#!/bin/bash

#pull base image
docker pull python:3.6

#-----------------------------
version=$(cat ../deploy/VERSION)

#build image
docker build -f ./BuildImageDockerfile -t phew_image:${version} .

