# Container2a - Image Labeling

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
6. [Usage](#usage)
7. [Data Flow](#data-flow)


## Introduction

This repository contains the Docker container setup for `Container2a - Image Labeling`. 

In the case that we are unable to directly pull pre-sorted datasets from Craigslist via container1, `label-studio` is a great alternate open source software to help streamline the process of manually labeling data for model training. In this setup, label studio is configured to pull unlabeled images from Google Cloud Bucket folder `unlabeled/` and upload the labeled images into folders `renovated/` and `unlabeled/`


## Features

- **Label Studio**: Fully-configured, latest stable version of Label Studio.
- **Google Cloud Storage**: Native integration for image retrieval and label storage.



## Prerequisites

- Docker
- Docker Compose
- Google Cloud Platform (GCP) Account
- Google Cloud Storage Bucket
- `gcloud` CLI tool or Google `Cloud Service Account Secret` JSON File



## Getting Started

### Set up Google Cloud Buckets/Folders
- In your GCP, go to the `Storage` tab on the left
- Click create new bucket or write down your bucket name
- Create three folders: `unlabeled/`, `fixer-upper/`, and `renovated/`


### Set up Google Cloud Credentials
- In your GCP console, go to `IAM & Admin` tab on the left
- Click on `Service Account`
- Create a new Service account, with the following roles/permissions:
    - `Storage Admin`
    - `GCP Token Creator`
- Save the new account. 
- Next, find the three dots on the newly created account and click manage keys.
- Create a new key, and download the JSON file.
- Save the JSON file in a `secrets` folder, structured like below


```
|-csa-data-labeling
|-secrets
```

### Build the Docker Image
- find the `docker-compose.yml` file and update the secrets and environment variables for your specific account
- For example:

```yml
GOOGLE_APPLICATION_CREDENTIALS: /secrets/gcp-rehab-ai-secret.json
GCP_PROJECT: "ac215-394023"
GCP_ZONE: "us-central1-a"
GCS_BUCKET_NAME: "rehab-image-detection-database"
```

### Run the Docker Container
- In a shell terminal, run the following command w/ the included `docker-shell.sh` file to start the container.


```bash
sh docker-shell.sh
```


## Usage

### Access Label Studio
- Open your web browser and navigate to `http://localhost:8080`.
- log in to label studio using the email and password setup in the `docker-compose.yml` file

### Connect to Google Cloud Storage
- Once logged in, create a new project
- Under the settings page, choose `import data` and select `Google Cloud Bucket`, and point to the `unlabeled/` folder
- For target folder, point to the `renovated/` and/or `fixer-upper/` folders
- save

### Set up labeling UI
- Under settings, select the option for setting up your labeling environment
- Select the `image classification` template to get started
- Update the label options to `fixer-upper` and `renovated`
- start labeling!


## Data Flow

- **Role**: Container2a - Image Labeling
- **Input**: Pulls images for manual labeling from the `unlabeled/` directory in the specified Google Cloud Bucket.
- **Output**: Saves labeled images back into the `fixer-upper/` and `renovated/` directories in the same Google Cloud Bucket.

