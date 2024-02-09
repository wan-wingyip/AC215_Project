#!/bin/bash

# make secrets folder
mkdir /home/evw754/secrets
mkdir /home/evw754/AC215_rehab_image_detection_ai/c2c-preprocessing/input_images
mkdir /home/evw754/AC215_rehab_image_detection_ai/c2c-preprocessing/output_images

# change permission to read and write for various folders
# change filepaths to your username
chmod a+rwx /home/evw754/secrets
chmod a+rwx /home/evw754/AC215_rehab_image_detection_ai/c2c-preprocessing/input_images
chmod a+rwx /home/evw754/AC215_rehab_image_detection_ai/c2c-preprocessing/output_images
