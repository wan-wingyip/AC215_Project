#!/bin/bash
############################
echo "Container is running!!!"

# Authenticate gcloud using service account
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# Set GCP Project Details
# --quiet inhibits the prompt for user input for 'yes'
gcloud config set project $GCP_PROJECT --quiet

echo "gcloud commands completed!!!"

#/bin/bash
pipenv shell && echo ""