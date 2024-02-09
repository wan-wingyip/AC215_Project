#!/bin/bash

set -e

# Create the network if we don't have it yet
docker network inspect vgg16-training-network >/dev/null 2>&1 || docker network create vgg16-training-network

# Build the image based on the Dockerfile
docker build -t vgg16-train-cli --platform=linux/arm64/v8 -f Dockerfile .

# Run All Containers
#### Note: add "winpty" in front of "docker-compose" into docker-shell.sh file, if run in Windows system
docker-compose run --rm --service-ports vgg16-train-cli