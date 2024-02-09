"""
Command line app that creates tf-records
"""
import os
import io
import argparse
import shutil
import json
#from PIL import Image
#import cv2
from google.cloud import storage

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

secrets_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
bucket_name = "rehab-image-detection-data"
input_images = "input_images"
output_images = "output_images"


# Function to clean filenames
def clean_filenames(input_dir):
    filenames = os.listdir(input_dir)
    for filename in filenames:
        if filename[-3:] != 'jpg':
            print(filename)
            filenames.remove(filename)
    
    return filenames


# function to create list of image paths and labels
def create_datalist(input_dir):
    # clean filenames in input_dir
    filenames = clean_filenames(input_dir)
    
    # init variables
    data_list = []
    ren_count = 0
    fix_count = 0

    # create tuple of filepath and label
    for filename in filenames:
        filepath = os.path.join(input_dir, filename)

        if filename[0:3] == 'ren':
            ren_count += 1
            tup = (0, filepath)
            data_list.append(tup)

        if filename[0:3] == 'fix':
            fix_count += 1
            tup = (1, filepath)
            data_list.append(tup)

    print("renovated pics:", ren_count)
    print("fixer-upper pics:", fix_count)

    return data_list


# Creates train, val and test set paths for TFrecords
def create_train_test_split(input_dir, test_percent):
    
    data_list = create_datalist(input_dir)

    # Create train and test set
    train_xy, test_xy = train_test_split(data_list, 
                                         test_size=test_percent, 
                                         random_state = 1)

    # print train set fixer upper %
    fix_class_count = 0
    for tup in train_xy:
        fix_class_count = fix_class_count + tup[0]
    print('Initial Train set images:', len(train_xy))    
    print('Initial Train set, Fixer-upper %:', round(fix_class_count/len(train_xy), 4))

    # print test set fixer upper %
    fix_class_count = 0
    for tup in test_xy:
        fix_class_count = fix_class_count + tup[0]
    print('Test set images:', len(test_xy))
    print('Test set, Fixer-upper %:', round(fix_class_count/len(test_xy), 4))

    # Create train and val set from previous train set
    train_xy, val_xy = train_test_split(train_xy, 
                                        test_size=test_percent, 
                                        random_state = 1)

    # print train set fixer upper %
    fix_class_count = 0
    for tup in train_xy:
        fix_class_count = fix_class_count + tup[0]
    print('Final Train set images:', len(train_xy))
    print('Final Train set, Fixer-upper %:', round(fix_class_count/len(train_xy), 4))

    # print val set fixer upper %
    fix_class_count = 0
    for tup in val_xy:
        fix_class_count = fix_class_count + tup[0]
    print('Val set images:', len(val_xy))
    print('Val set, Fixer-upper %:', round(fix_class_count/len(val_xy), 4))

    return train_xy, val_xy, test_xy


# Creates tf_example for writing to tfrecords
def create_tf_example(item, num_channels, pixels):
  
  num_channels = num_channels
  image_height = pixels
  image_width = pixels

  # Read image
  image = tf.io.read_file(item[1])
  image = tf.image.decode_jpeg(image, channels=num_channels)
  image = tf.image.resize(image, [image_height,image_width])
  # # Encode
  # image = tf.cast(image, tf.uint8)
  # image = tf.image.encode_jpeg(image, optimize_size=True, chroma_downsampling=False)
  image = tf.cast(image, tf.uint8)

  # Label
  # label = label2index[item[0]]
  label = item[0]

  # Build feature dict
  feature_dict = {
      'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image.numpy().tobytes()])),
      'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
  }

  example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
  return example


# Helper function that creates tf records
def create_tfrecords_helper(data, 
                            num_shards, 
                            prefix, 
                            output_folder,
                            num_channels,
                            pixels):
  
  num_channels = num_channels
  pixels = pixels
  num_records = len(data)
  step_size = num_records//num_shards + 1

  for i in range(0, num_records, step_size):
    print("Creating shard:",(i//step_size)," from records:",i,"to",(i+step_size))
    path = '{}/{}_000{}.tfrecords'.format(output_folder, prefix, i//step_size)
    print(path)

    # Write the file
    with tf.io.TFRecordWriter(path) as writer:
      # Filter the subset of data to write to tfrecord file
      for item in data[i:i+step_size]:
        tf_example = create_tf_example(item, num_channels, pixels)
        writer.write(tf_example.SerializeToString())


# Function that calls above helper functions in succession
def create_tfrecords_full():

    # bring in command line arguments and other variables
    pixels = args.pixel_size
    num_channels = args.num_chan
    test_percent = args.test_percent
    input_dir = output_images
    output_folder = 'tf-records'

    # get train test split filepaths and labels
    train_xy, val_xy, test_xy = create_train_test_split(input_dir, test_percent)

    # make tfrecords output directory
    os.makedirs('tf-records', exist_ok=True)    
    
    # Create train tf_records
    create_tfrecords_helper(train_xy, 
                            num_shards=5, 
                            prefix='train', 
                            output_folder=output_folder,
                            num_channels=num_channels,
                            pixels=pixels)

    # Create val tf_records
    create_tfrecords_helper(val_xy, 
                            num_shards=2, 
                            prefix='val', 
                            output_folder=output_folder,
                            num_channels=num_channels,
                            pixels=pixels)

    # Create test tf_records
    create_tfrecords_helper(test_xy, 
                            num_shards=2, 
                            prefix='test', 
                            output_folder=output_folder,
                            num_channels=num_channels,
                            pixels=pixels)

    print('finished creating tf-records')


def upload():
    print("upload")

    # Upload to bucket
    client = storage.Client.from_service_account_json(secrets_json)
    bucket = client.bucket(bucket_name)
    local_dir = 'tf-records'

    # Get the list of filenames from local dir
    filenames = os.listdir(local_dir)

    count = 0
    for filename in filenames:
        count += 1

        # Create GCP destination path and blob object
        destination_path = os.path.join('tf-records', filename)
        blob = bucket.blob(destination_path)

        # Get filepath to upload
        filepath = os.path.join(local_dir, filename)

        # Upload filepath to GCP
        blob.upload_from_filename(filepath)

    # Clear
    print('Files uploaded:', count)
    shutil.rmtree(local_dir, ignore_errors=True, onerror=None)



def main(args=None):
    print("Args:", args)

    if args.create_tfrecords_full:
        create_tfrecords_full()
    if args.upload:
        upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Create and upload tfrecords")

    parser.add_argument(
        "-ctf", "--create_tfrecords_full", action="store_true", help="creates tf records"
    )
    
    parser.add_argument(
        "-ps", "--pixel_size", type=int, default=224, help="Image pixel size"
    )

    parser.add_argument(
        "-nc", "--num_chan", type=int, default=3, help="Number image channels"
    )

    parser.add_argument(
        "-tp", "--test_percent", type=float, default=0.2, help="Train Test Split %"
    )

    parser.add_argument(
        "-f", "--foldername", type=str, help="Folder to pull images from or push to"
    )

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload files text to GCS bucket",
    )

    args = parser.parse_args()

    main(args)