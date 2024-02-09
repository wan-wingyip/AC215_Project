#!/bin/bash

# Use this script to automatically build and tag the Docker image, and push it to Docker Hub.

# Exit immediately if a command exits with a non-zero status
set -e

# Check if already logged in to Docker Hub
if docker info --format '{{.IndexServerAddress}}' | grep 'https://index.docker.io/v1/' > /dev/null 2>&1; then
    echo "Already logged in to Docker Hub, skipping login and starting build..."
else
    echo "Not logged in to Docker Hub, login first."
    read -p "Enter your Docker Hub username: " username
    read -s -p "Enter your Docker Hub password: " password
    echo
    docker login -u "$username" -p "$password"
fi

# Build the Docker image and tag it
docker buildx build -t fk798/c4-model-inference:ms5 --platform=linux/amd64 -f Dockerfile .
echo "Building and tagging complete."

# Push to Docker Hub - currently set to Tony's repo but change to env variables in next version.
docker push fk798/c4-model-inference:ms5
echo "Pushed to Docker Hub!"