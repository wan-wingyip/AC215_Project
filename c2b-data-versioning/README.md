# Real Estate Image Data Versioning with DVC

## Overview

This Docker container is designed to manage data versioning for our real estate images. It uses [DVC (Data Version Control)](https://dvc.org/) to help keep track of changes in the dataset over time. 

### Role

Manages versioning for labeled data to keep track of changes.

#### Trigger

- Automatically triggered when new images are downloaded from the `fixer-upper/` or `renovated/` folders on our Google Cloud Storage bucket.

#### Result

- The dataset version is incremented by 1 (e.g., v1, v2, v3, etc.).
- The new dataset version is tracked in a data registry folder named `dvc-store/` located in the same Google Cloud Storage bucket.



## Features

- Automated versioning: Automatically versions the dataset with an incremented version number.
- Data Registry: Utilizes a `dvc-store/` folder to maintain versions.
- Cloud Storage: Seamlessly integrates with Google Cloud Storage for easy data management.



## Pre-requisites

- Docker installed on your machine.
- Google Cloud Storage Bucket set up with appropriate permissions.
- Service Account Key for Google Cloud Storage authentication.

## Setup Instructions

### Set up Google Cloud Buckets/Folder
- In your GCP, go to the `Storage` tab on the left
- Click create new bucket or write down your bucket name
- Create a new folder: `dvc-store/`


### Set up Google Cloud Credentials (if not set up yet!)
You can reuse the same credentials as before but if not:

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
|-c2b-data-versioning
|-secrets
```

### Build the Docker Image
- find the `cli.py` and `docker-shell.sh` file and update the secrets and environment variables for your specific account as needed
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

### Initialize Data Registry
- Initialize your data registry using DVC
    ```bash
    dvc init
    ```

### Configure Google Cloud Storage as remote registry
- Add your GCS Bucket as a remote registry for your dataset
    ```bash
    dvc remote add -d renovated gs://your-bucket-name/dvc-store
    dvc remote add -d fixer-upper gs://your-bucket-name/dvc-store
    ```

### Add dataset to registry
- Add image dataset to the DVC registry
    ```bash
    dvc add fixer-upper/
    dvc add renovated/
    ```

### Push data to remote registry
- Push your dataset to your remote registry on GCS
    ```bash
    dvc push
    ```
- Go to your GCS Bucket folder `dvc-store/` to view the tracking files

### Update Git to track DVC
- Check the git status
    ```bash
    git status
    ```
- Add and commit changes
    ```
    git add .
    git commit -m 'Initial dataset versioning'
    ```
- Tag the dataset version
    ```
    git tag -a 'dataset_v1' -m 'tag for dataset version 1'
    ```
- Push changes to Git
    ```
    git push --atomic origin main dataset_v1
    ```


## To update dataset version / work with new data
- Download newly annotated data
    ```
    # your download scripts here, if necessary
    ```
- Add the updated dataset to the registry
    ```
    dvc add fixer-upper/
    dvc add renovated/
    ```

- Push the updated data to the remote registry
    ```
    dvc push
    ```

### Update Git to track DVC changes
- Check git status
    ```
    git status
    ```
- Add and commit changes
    ```
    git add .
    git commit -m 'Added newly annotated data'
    ```
- Tag the new dataset version
    ```
    git tag -a 'dataset_v2' -m 'tag for dataset version 2'
    ```
- Push changes to Git
    ```
    git push --atomic origin main dataset_v2
    ```

