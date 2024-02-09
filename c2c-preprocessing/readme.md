##c2c-preprocessing - Preprocessing Container

This container downloads images from GCP bucket, resizes the images, and re-uploads to GCP bucket. 

To use this docker container, please build from the dockerfile in this folder and run the resulting docker image.

Preprocess.py has three functions: (1) to download images (-d), (2) resize images (-r), and (3) upload them (-u) to GCP bucket. 

Currently, the images are set to 224x224 and RGB for training, though this can be changed in the future if necessary to speed up training.

Secrets json file required for GCP authentication has not been included in this container.


To run this on GCP VM:

1. Create VM instance on GCP, and SSH into VM instance

2. Run the following:
sudo apt-get update
sudo apt install git

3. Go to Github.com and create Personal Access Token
- This is used to pull from private repos 
- Make sure to allow for read write access in the permissions for the specific repo you want to clone

4. Clone git repo into VM by running the following:
git clone -b milestone3 https://<insert personal access token>@github.com/wan-wingyip/AC215_rehab_image_detection_ai.git

5. cd into c2c-preprocess folder and run sh script vm.sh and dir.sh
cd c2c-preprocessing
sh vm.sh
sh dir.sh

6. Build and run docker file inside c2c-preprocess folder
docker build -t c2c -f Dockerfile .
docker run -v /home/evw754/secrets:/app/secrets --rm -ti --mount type=bind,source="$(pwd)",target=/app c2c

6a. Init DVC, and add to dvc registry, run the dvc init and dvc remote add before running step 8 (resize). Run dvc add output_images and dvc push after running step 8 (resize)
# initialize dvc in git repo
dvc init
# Add remote registry to GCS bucket
dvc remote add -d output_images gs://ac215-rehab-preprocess/dvc_store
# Add dataset to registry
dvc add output_images
# Push Data to remote registry
dvc push

7. Inside container, preprocess.py will download images and create a directory called input_images and save those images in that directory. Run the following:
python preprocess.py -d -f renovated
-d flag is to signify download
-f flag is to signify which GCP folder to download from

8. To resize images, run the following: 
python preprocess.py -r -s 224
-r flag is to signify resizing
-s flag is to signify the pixel size of the image. Default is 224, and the images will be 224x224.

9. To upload images, run the following: 
python preprocess.py -u -f renovated-processed
-u flag is to signify upload from GCP
-f flag is to signify which GCP folder to upload to





