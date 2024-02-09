#!/bin/bash

echo "Container is running!!!"

# Authenticate gcloud using service account
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# Set GCP Project Details
gcloud config set project $GCP_PROJECT

# Configure GCR
gcloud auth configure-docker gcr.io -q

echo "Container is authenticated with GCP, starting shell!!!"

#/bin/bash
pipenv shell

#!/bin/sh (scrapes data from craigslist)
python cli.py -s

#!/bin/sh (uploads data to GCS)
python cli.py -u