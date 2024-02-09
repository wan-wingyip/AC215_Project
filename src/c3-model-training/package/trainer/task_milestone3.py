import argparse
import os
import requests
import zipfile
import tarfile
import time

# Tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.utils.layer_utils import count_params

# fixer related
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input, Flatten, Dense
import scipy

# sklearn
from sklearn.model_selection import train_test_split

# Tensorflow Hub
import tensorflow_hub as hub

# W&B
import wandb
from wandb.keras import WandbCallback, WandbMetricsLogger


# Setup the arguments for the trainer task
parser = argparse.ArgumentParser()
parser.add_argument(
    "--model-dir", dest="model_dir", default="test", type=str, help="Model dir."
)
parser.add_argument("--lr", dest="lr", default=0.001, type=float, help="Learning rate.")
parser.add_argument(
    "--model_name",
    dest="model_name",
    default="mobilenetv2",
    type=str,
    help="Model name",
)
parser.add_argument(
    "--train_base",
    dest="train_base",
    default=False,
    action="store_true",
    help="Train base or not",
)
parser.add_argument(
    "--epochs", dest="epochs", default=10, type=int, help="Number of epochs."
)
parser.add_argument(
    "--batch_size", dest="batch_size", default=16, type=int, help="Size of a batch."
)
parser.add_argument(
    "--wandb_key", dest="wandb_key", default="16", type=str, help="WandB API Key"
)
args = parser.parse_args()

# TF Version
print("tensorflow version", tf.__version__)
print("Eager Execution Enabled:", tf.executing_eagerly())
# Get the number of replicas
strategy = tf.distribute.MirroredStrategy()
print("Number of replicas:", strategy.num_replicas_in_sync)

devices = tf.config.experimental.get_visible_devices()
print("Devices:", devices)
print(tf.config.experimental.list_logical_devices("GPU"))

print("GPU Available: ", tf.config.list_physical_devices("GPU"))
print("All Physical Devices", tf.config.list_physical_devices())


# Utils functions
def download_file(packet_url, base_path="", extract=False, headers=None):
    if base_path != "":
        if not os.path.exists(base_path):
            os.mkdir(base_path)
    packet_file = os.path.basename(packet_url)
    with requests.get(packet_url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(os.path.join(base_path, packet_file), "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    if extract:
        if packet_file.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(base_path, packet_file)) as zfile:
                zfile.extractall(base_path)
        else:
            packet_name = packet_file.split(".")[0]
            with tarfile.open(os.path.join(base_path, packet_file)) as tfile:
                tfile.extractall(base_path)

##################################################################
from google.cloud import storage
storage_client = storage.Client()                    # Initialize the Google Cloud Storage client

def download_folder_from_gcs(bucket_name, source_folder_path, destination_folder_path):
    """
    Downloads a folder from Google Cloud Storage to a local directory.

    :param bucket_name: Name of the GCS bucket.
    :param source_folder_path: Path in GCS of the folder you want to download.
    :param destination_folder_path: Local path where the folder should be downloaded.
    """
    
    # Initialize the GCS client
    #storage_client = storage.Client.from_service_account_json(path_to_secret_key)
    bucket = storage_client.bucket(bucket_name)
    
    # Get the list of files from the source folder path in GCS
    blobs = bucket.list_blobs(prefix=source_folder_path)
    
    for blob in blobs:
        # Check if the blob is a directory itself
        if not blob.name.endswith('/'):
            # Construct the full local path
            local_file_path = os.path.join(destination_folder_path, os.path.relpath(blob.name, source_folder_path))
            local_dir = os.path.dirname(local_file_path)
            
            # Create local directories if they don't exist
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            
            # Download the file
            blob.download_to_filename(local_file_path)
            print(f"File {blob.name} downloaded to {local_file_path}.")

# Example usage:
# download_folder_from_gcs('my_bucket', prefix_fixers, 'fixers_download_from_gcs')


## bucket_name is the bucket you are donwloading from. 
## prefix is the folder you want to download from.  
## the last arguement is which folder you want things downloaded into.
## download_folder_from_gcs(bucket_name, prefix_fixers, 'fixers_download_from_gcs')  
download_folder_from_gcs('lec8_bucket', 'craigslist images/fixer_uppers/', 'fixers_download_from_gcs')  
download_folder_from_gcs('lec8_bucket', 'craigslist images/renovated/', 'renovated_download_from_gcs')  



##################################################################
## to read in image files from bucket
##
## label for fixer = 0
## label for renovated = 1

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from tensorflow.keras.preprocessing import image
import io

# # Paths to the main folders
# renovated_path = 'craigslist images/renovated'
# fixer_path = 'craigslist images/fixer_uppers'

# from google.cloud import storage
# client = storage.Client()                    # Initialize the Google Cloud Storage client
# bucket = client.get_bucket('lec8_bucket')    # Get a reference to the GCS bucket

# # renovated_blob = bucket.list_blobs(prefix=renovated_path)     # List the contents in the bucket
# # fixer_blob     = bucket.list_blobs(prefix=fixer_path)         # List the contents in the bucket

# # renovated_images = []
# # for renovated in renovated_blob:
# #     renovated_images.append(renovated.name)

# # fixer_images = []
# # for fixer in fixer_blob:
# #     fixer_images.append(fixer.name)


# # renovated_images = list(bucket.list_blobs(prefix=renovated_path))     # List the contents in the bucket
# # fixer_images     = list(bucket.list_blobs(prefix=fixer_path))         # List the contents in the bucket




##################################################################
dest_renovated   = 'renovated_download_from_gcs'
dest_fixer_upper = 'fixers_download_from_gcs'

renovated_images = []
for root, dirs, files in os.walk(dest_renovated):
    for file in files:
        # ensure file is an image
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            renovated_images.append(os.path.join(root, file))

fixer_images = []
for root, dirs, files in os.walk(dest_fixer_upper):
    for file in files:
        # ensure file is an image
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            fixer_images.append(os.path.join(root, file))

##################################################################


# Generate a list of labels and full paths to images
data_list = []
for label,prop_type in enumerate(['fixer','renovated']):
  if prop_type == 'fixer':
    data_list.extend([(label,f) for f in fixer_images])
  elif prop_type == 'renovated':
    data_list.extend([(label,f) for f in renovated_images])

## sanity check
print("Full size of the dataset:",len(data_list))
print("data_list (fixer):",data_list[0:2])
print("data_list (renovated):",data_list[-2:])


##################################################################
## This imshow() section does not seem to work to display images
##
# Generate a random sample of index
image_samples = np.random.randint(0,high=len(data_list)-1, size=12)

fig = plt.figure(figsize=(20,8))
for i,img_idx in enumerate(image_samples):
    axs = fig.add_subplot(3,4,i+1)
    axs.set_title(data_list[img_idx][0])
    # Read image
    image = plt.imread(data_list[img_idx][1])

    plt.imshow(image)
    plt.axis('off')
    print("matplotlib should show images here ...")

plt.suptitle("Sample Images")
plt.show()
print("matplotlib finished here ...")


##################################################################
## to generate data_x & data_y

# Each element in data_x is the path to the image
# Each element in data_y is the label of that image

# Build data x, y
data_x = [itm[1] for itm in data_list]
data_y = [itm[0] for itm in data_list]

## sanity check
print("data_x:",len(data_x))
print("data_y:",len(data_y))
print("data_x:",data_x[:5])
print("data_y:",data_y[:5])


##################################################################
## Train_test_split()
test_percent = 0.10
validation_percent = 0.2

# Split data into train / test
train_validate_x, test_x, train_validate_y, test_y = train_test_split(data_x,
                                                                      data_y,
                                                                      test_size=test_percent)

# Split data into train / validate
train_x, validate_x, train_y, validate_y = train_test_split(train_validate_x,
                                                            train_validate_y,
                                                            test_size=test_percent)

## sanity check
print("train_x count:",len(train_x))
print("validate_x count:",len(validate_x))
print("test_x count:",len(test_x))


##################################################################
## To create TF datasets
def get_dataset(image_width = 224, image_height = 224, num_channels = 3, batch_size = 32):

  # Load Image
  def load_image(path, label):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=num_channels)
    image = tf.image.resize(image, [image_height,image_width])
    return image, label

  # Normalize pixels (not used. images are scaled in pre-processor)
  def normalize(image, label):
    image = image/255
    return image, label

  train_shuffle_buffer_size= len(train_x)
  validation_shuffle_buffer_size= len(validate_x)

  # Create TF Dataset
  train_data = tf.data.Dataset.from_tensor_slices((train_x, train_y))
  validation_data = tf.data.Dataset.from_tensor_slices((validate_x, validate_y))
  test_data = tf.data.Dataset.from_tensor_slices((test_x, test_y))

  #############
  # Train data
  #############
  # Apply all data processing logic
  train_data = train_data.cache()\
                        .shuffle(buffer_size=train_shuffle_buffer_size)\
                        .map(load_image, num_parallel_calls=tf.data.AUTOTUNE)\
                        .batch(batch_size)\
                        .prefetch(tf.data.AUTOTUNE)\

  ##################
  # Validation data
  ##################
  # Apply all data processing logic
  validation_data = validation_data.cache()\
                        .shuffle(buffer_size=validation_shuffle_buffer_size)\
                        .map(load_image, num_parallel_calls=tf.data.AUTOTUNE)\
                        .batch(batch_size)\
                        .prefetch(tf.data.AUTOTUNE)\

  ############
  # Test data
  ############
  # Apply all data processing logic
  test_data = test_data.cache()\
                        .map(load_image, num_parallel_calls=tf.data.AUTOTUNE)\
                        .batch(batch_size)\
                        .prefetch(tf.data.AUTOTUNE)\

  return (
      train_data, validation_data, test_data
  )


##################################################################
# Login into wandb
wandb.login(key=args.wandb_key)


##################################################################
## model definition (compile(), fit())

## train & save weights into wandb.ai
from tensorflow.keras.layers import Input, Flatten, Dense
from tensorflow.keras.models import Sequential, Model

## transfer learning from keras VGG16 model weights
model_name = args.model_name
train_base = args.train_base
learning_rate = args.lr
img_height = 224
img_width  = 224
img_channel = 3                 ## imagenet is trained on RGB
batch_size = args.batch_size
epochs = args.epochs

# Free up memory
K.clear_session()

# Data
train_data, validation_data, test_data = get_dataset(image_width = img_width,
                                                     image_height = img_height,
                                                     num_channels = img_channel,
                                                     batch_size = batch_size)

# invoke VGG16
new_input = Input(shape=(img_height, img_width, img_channel))
base_model = VGG16(weights='imagenet', input_tensor=new_input, include_top=False)
base_model.summary()

# base layers + 3 FC layers
x = Flatten()(base_model.layers[-1].output)

# Add a fully connected layer with 1024 units and ReLU activation
x = Dense(units=1024, activation='relu')(x)
x = Dense(units=1024, activation='relu')(x)
x = Dense(units=1024, activation='relu')(x)

# Add a final output layer with the desired number of classes and sigmoid activation
output = Dense(units=1, activation='sigmoid')(x)

# Create the final model by combining the VGG16 base model with the newly added layers
fixer_model = Model(inputs=base_model.input, outputs=output, name=model_name+'_'+str(train_base))

# fix all weights in base_model
for layer in base_model.layers:
    layer.trainable = False

# Compile the model with appropriate loss, optimizer, and metrics
fixer_model.compile(optimizer = Adam(),
                    loss = 'binary_crossentropy',
                    metrics = ['acc'])

# Initialize a W&B run
wandb.init(
    project = 'rehab-ai-main',
    config = {
      "learning_rate": learning_rate,
      "epochs": epochs,
      "batch_size": batch_size,
      "model_name": fixer_model.name
    },
    name = fixer_model.name
)

# Train the model on the training data and validate on the validation data
start_time = time.time()
history = fixer_model.fit(train_data,
                          validation_data=validation_data,
                          callbacks=[WandbCallback()],
                          verbose=1,
                          epochs=epochs)

execution_time = (time.time() - start_time)/60.0
print("Training execution time (mins)",execution_time)

# Update W&B
wandb.config.update({"execution_time": execution_time})

# Close the W&B run
wandb.run.finish()


##################################################################
print("Training Job Complete")
