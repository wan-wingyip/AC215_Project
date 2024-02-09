#!/bin/bash


# This script automatically builds, tags, and pushes a Docker image Google Artifact Registry!

# Exit immediately if a command exits with a non-zero status
set -e

# Build the Docker image and tag it
# Syntax: docker buildx build -t <dockerhub-username>/<docker-hub-repo>:<tag> --platform=linux/amd64 -f <dockerfile-name> .
docker buildx build -t tonyahu/rehab-ai:c4-latest --platform=linux/amd64 -f ../src/c4-model-inference/Dockerfile .
echo "Building complete."

# Check if already logged in to Google Artifact Registry
if docker info --format '{{.IndexServerAddress}}' | grep 'https://us-central1-docker.pkg.dev/' > /dev/null 2>&1; then
    echo "Already logged in to Google Artifact Registry, skipping login and starting build..."
else
    echo "Not logged in to Google Artifact Registry, please follow instructions to login first."
    gcloud auth login
    gcloud auth configure-docker us-central1-docker.pkg.dev
    echo "Configured Google Artifact Registry for us-central1!"
fi

# Tag the image for Google Artifact Registry
# Syntax: docker tag <dockerhub-username>/<docker-hub-repo>:<tag> <artifact-repo-region>-docker.pkg.dev/<gcp-project-id>/<artifact-repo>/<image-name>:<tag>
echo "Now retagging the docker image for Google Artifact Registry!"
docker tag tonyahu/rehab-ai:c4-latest us-central1-docker.pkg.dev/ac215-399020/vertex-ai-pipeline/c4-model-inference:latest
echo "Retagging complete!"

# Push the image to Google Artifact Registry
# Syntax: docker push <artifact-repo-region>-docker.pkg.dev/<gcp-project-id>/<artifact-repo>/<image-name>:<tag>
docker push us-central1-docker.pkg.dev/ac215-399020/vertex-ai-pipeline/c4-model-inference:latest
echo "Pushed to Google Artifact Registry successfully!"
echo "View at https://console.cloud.google.com/artifacts/docker/ac215-399020/us-central1/vertex-ai-pipeline?project=ac215-399020"

# Exit the script
exit 0
