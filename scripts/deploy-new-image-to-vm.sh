# Run this script to update the docker images on a GCP VM instance to the latest image.
# Env variables should be passed in via Github Actions CLI or Github Secrets.
# Best paired after running any build-tag-push.sh script if we want to deploy changes.
# Note: Server might be offline temporarily during the update image and pruning process, so run at a inconspicuous time.

# # command to update docker images on a VM instance to the latest version
# gcloud compute instances update-container $INSTANCE_NAME --zone $INSTANCE_ZONE --container-image $ARTIFACT_REGISTRY:$BUILD_ID

# # command to prune old docker images from a VM instance to save space
# gcloud compute ssh $INSTANCE_NAME --zone $INSTANCE_ZONE --command 'docker system prune -f -a'



# Check if logged in to Google Cloud
if docker info --format '{{.IndexServerAddress}}' | grep 'https://us-central1-docker.pkg.dev/' > /dev/null 2>&1; then
    echo "Already logged in to Google Cloud, skipping login and starting deployment..."
else
    echo "Not logged in to Google Artifact Registry, please follow instructions to login first."
    gcloud auth login
fi

# command to update docker images on a VM instance to the latest version
gcloud compute instances update-container c5b-front-end --zone us-central1-a --container-image vertex-ai-pipeline:c5b-front-end:latest

# command to prune old docker images from a VM instance to save space
gcloud compute ssh c5b-front-end --zone us-central1-a --command 'docker system prune -f -a'
