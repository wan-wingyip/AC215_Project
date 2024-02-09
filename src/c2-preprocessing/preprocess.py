"""
Command line app that downloads and resizes images
"""
import os
import io
import argparse
import shutil
import json
from PIL import Image
import subprocess
import time

#import cv2
from google.cloud import storage
#from google.oauth2.service_account import Credentials

from tempfile import TemporaryDirectory

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

secrets_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
bucket_name = "rehab-image-detection-data"
input_images = "input_images"
output_images = "output_images"


def makedirs():
    os.makedirs(input_images, exist_ok=True)
    os.makedirs(output_images, exist_ok=True)

def get_folder_size(base_path):
  folder_size = subprocess.check_output(['du','-sh', base_path]).split()[0].decode('utf-8')
  return folder_size

def download():
    # function will print name of every 500 images
    # function will also print total count
    print("downloading")

    # Clear
    # shutil.rmtree(input_images, ignore_errors=True, onerror=None)
    makedirs()

    # start time
    start_time = time.time()

    # Create client
    client = storage.Client.from_service_account_json(secrets_json)
    bucket = client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=args.foldername + "/")
    count = 0
    for blob in blobs:
        count += 1
        if count % 500 == 0 :
            print(count, ": ", blob.name)
        if not blob.name.endswith("/"):
            filename = str(blob.name)
            filename = filename.replace(args.foldername, args.foldername[:3])
            filename = filename.replace("/","")
            filename = filename.replace("image","")
            filename = input_images + "/" + filename
            blob.download_to_filename(filename)
    
    folder_size = get_folder_size(input_images)
    
    execution_time = (time.time() - start_time)/60.0
    
    print("finished downloading")
    print("Image count:", count)
    print("Folder  size:", folder_size)
    print("Execution time (mins)",execution_time)
    

def resize():
    print("resize")
    
    # remove current output_images folder
    shutil.rmtree(output_images, ignore_errors=True, onerror=None)

    # create new empty output_images folder
    makedirs()

    # Get the list of image files
    image_files = os.listdir(input_images)

    # resize
    ps = args.pixel_size
    for image_file in image_files:
        img = Image.open(input_images + '/' + image_file)
        resized_img = img.resize((ps,ps))
        resized_img.save('output_images/' + image_file, 'JPEG')


#def resize():
#    print("resize")
#    makedirs()
#
#    # Get the list of image files
#    image_files = os.listdir(input_images)
#
#    # resize
#    for image_file in image_files:
#        img = cv2.imread(input_images + '/' + image_file)
#        resized_img = cv2.resize(img, (224,224))
#        cv2.imwrite('output_images/' + image_file, resized_img)


# def upload():
#     print("upload")

#     # Upload to bucket
#     client = storage.Client.from_service_account_json(secrets_json)
#     bucket = client.bucket(bucket_name)

#     # Get the list of text file
#     resized_image_files = os.listdir(output_images)

#     count = 0
#     for resized_image in resized_image_files:
#         count += 1
    
#         filename = os.path.join(output_images, resized_image)
#         destination_blob_name = os.path.join(args.foldername, resized_image)
        
#         if count % 10 == 0 :
#             print(blob.name)
        
#         blob = bucket.blob(destination_blob_name)
#         blob.upload_from_filename(filename)
    
#     # Clear
#     print('Finished Uploading')
#     shutil.rmtree(output_images, ignore_errors=True, onerror=None)
#     makedirs()


def main(args=None):
    print("Args:", args)

    if args.download:
        download()
    if args.resize:
        resize()
    # if args.upload:
    #     upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Download, resize, and upload images")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download files from GCS bucket",
    )

    parser.add_argument(
        "-r", "--resize", action="store_true", help="Resize images to 224x224"
    )
    
    parser.add_argument(
        "-ps", "--pixel_size", type=int, default=224, help="Image pixel size"
    )

    parser.add_argument(
        "-f", "--foldername", type=str, help="Folder to pull images from or push to"
    )

    args = parser.parse_args()

    main(args)
