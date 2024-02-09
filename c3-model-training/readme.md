# Model (vgg16): model training

## Prerequisites
* Have Docker installed
* Cloned this repository to your local machine with a terminal up and running
* Check that your Docker is running with the following command

`docker run hello-world`

## Ensure Docker Memory
- To make sure we can run multiple container go to Docker>Preferences>Resources and in "Memory" make sure you have selected > 4GB

## Clone the github repository
- Clone or download from [here](https://github.com/tonyhua18/AC215_rehab_image_detection_ai/vgg16_training)

## Prepare Dataset
Our teammate will prepare images files and save them in a GCS bucket.
Therefore, the ML (vgg16) model needs to have permission to access this bucket.

More details to be provided. 

## Download Labeled Data
Our team currently has two alternatives:
1) Use the paid Google service, Colab Pro or Colab Pro+, to accelerate the training.
2) Use local GPU resources that some of our teammates own.

- There are pros and cons with either choice. Colab perhaps is easier to set up, but with recurring cost. Customized systems need configuration and may run into unseen issues that are irrelevant to this class.
So depending on needs and other contraints, we'll decide accordingly.
- Regardless, we'll need to download or provide access to the images for training the model.

More details to be provided

## Docker Cleanup
To make sure we do not have any running containers and clear up an unused images
* Run `docker container ls`
* Run `docker system prune`             ## Stop any container that is running
* Run `docker image ls`

## To start the container
#### Note: add "winpty" in front of "docker-compose" into docker-shell.sh file, if run in Windows system
* sh docker-shell.sh

## To version the weights & hyperparameters
More details to be provided


