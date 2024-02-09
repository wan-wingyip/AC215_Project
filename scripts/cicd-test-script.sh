#!/bin/bash


# This is a test script to test the cicd-pipeline-demo

# Exit immediately if a command exits with a non-zero status
set -e

# Check if logged in to Docker Hub
if docker info --format '{{.IndexServerAddress}}' | grep 'https://index.docker.io/v1/' > /dev/null 2>&1; then
    echo "Already logged in to Docker Hub, skipping login and starting build..."
else
    echo "Not logged in to Docker Hub."
fi


# Check if logged in to Google Artifact Registry
if docker info --format '{{.IndexServerAddress}}' | grep 'https://us-central1-docker.pkg.dev/' > /dev/null 2>&1; then
    echo "Already logged in to Google Artifact Registry, skipping login and starting build..."
else
    echo "Not logged in to Google Artifact Registry, please follow instructions to login first."
fi


# Send a complete message to the console
echo "Test script complete!"

# Exit the script
exit 0
