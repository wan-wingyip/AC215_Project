# AC215- Rehab Image Detection AI

For Milestone 2 - See branch `milestone2`
For Milestone 3 - See branch `milestone3`
- specific container updates are available in each folder!

## Table of Contents

- [Objective](#objective)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Project Pipeline](#project-pipeline)
- [Getting Started](#getting-started)
- [License](#license)

## Objective

We built a CNN (Convolutional Neural Network) model that predicts whether a home is renovated or not, solely based on an image. This model will be integrated into a web platform allowing end users to search for real estate properties by zip code, curated for their preference of renovated vs. un-renovated homes.

The feature targets a gap in the real estate market, empowering everyday home buyers to more accessibly search for fixer-upper homes that offer significant investment potential, a strategy that is currently limited to savvy real estate investors.

## Tech Stack

- Docker
- Python
- TensorFlow
- React.js
- Google Cloud Platform

## Prerequisites

- Docker
- Google Cloud SDK
- Node.js
- Python 3.x

## Project Pipeline

### Container1 - Training Data Scraper

**Role**: Scrapes images of renovated and un-renovated homes from Craigslist for model training.
- **Source**: Craigslist
- **Output**: Saves images to Google Cloud Bucket in the `fixer-upper/` and `renovated/` folders.


### Container2a - Image Labeling

**Role**: Pulls images for manual labeling and saves them back labeled in the case that we have unlabeled data.
- **Input**: Pulls from `unlabeled/` in Google Cloud Bucket.
- **Output**: Saves to `fixer-upper/` and `renovated/` in Google Cloud Bucket.

### Container2b - Data Versioning

**Role**: Manages versioning for labeled data to keep track of changes.
- **Trigger**: New images are downloaded from the `fixer-upper/` or `renovated/` folders for training
- **Result**: Dataset version is incremented by 1 (e.g. v1, v2, v3, etc) and tracked in a data registry folder `dvc-store/` on Google Cloud bucket, using the open-source DVC software.


### Container2c - Data Preprocessing

**Role**: Resizes images to correct dimensions for CNN Model Architecture
- **Input**: Pulls unprocessed images from `fixer-upper/` and `renovated/` in Google Cloud Bucket.
- **Output**: Saves resized images to `fixer-upper/` and `renovated/` in Google Cloud Bucket.


### Container3 - CNN Model Training

**Role**: Trains the CNN model to identify fixer-upper homes using the labeled images.
- **Input**: Pulls images from `fixer-upper/` and `renovated/` in Google Cloud Bucket.
- **Output**: Trained model.


### Container4 - CNN Model Inference

**Role**: Hosts the most accurate trained model and performs inferences on unseen images.
- **Input**: Unseen images from user selected zip code, fetched by container5.
- **Output**: Labels applied to images indicating if renovated or fixer-upper.


### Container5 - Fetch home listings from API

**Role**: Fetches home listings from a real estate API for a user selected zip code
- **Input**: A user selected zip code
- **Output**: Fetched home listings, including images, from a real estate API


### Container6 - Landing Page Frontend

**Role**: Serves the web platform where users can search for properties.
- **Input**: End users enter a zip code to search for properties.
- **Output**: Website will return a list of un-renovated, fixer-upper homes in the area.


## Getting Started

The project and its model are still in development. For a more in-depth understanding of each container's role and setup instructions, please refer to the individual `readme` files located within each container's respective folder. Thank you for your excitement!

## License

MIT License. See `LICENSE` for more information.
