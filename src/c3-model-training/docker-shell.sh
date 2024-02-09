#!/bin/bash

export IMAGE_NAME=fixer-model-training-cli
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../secrets/
#export GCS_BUCKET_URI="gs://lec8_bucket"
export GCS_BUCKET_URI="gs://rehab-image-detection-data"
#export GCP_PROJECT="ac215-mleung-398423"
export GCP_PROJECT="ac215-399020"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

# Run Container

winpty docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=../secrets/gcp-rehab-ai-secret.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_URI=$GCS_BUCKET_URI \
-e WANDB_KEY=$WANDB_KEY \
$IMAGE_NAME