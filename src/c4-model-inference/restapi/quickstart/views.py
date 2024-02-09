from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import requests
import tensorflow as tf
import numpy as np
import wandb
import os
from dotenv import load_dotenv


# Try to load WANDB from .env file first
load_dotenv()
WANDB_API_KEY = os.getenv("WANDB_API_KEY")

# If the API key is not found in the .env file, try to load from the .txt file
if not WANDB_API_KEY:
    secret_file = "../secrets/wb.txt"
    with open(secret_file, "r") as file:
        WANDB_API_KEY = file.readline().strip()

# Check if the API key was successfully loaded
if not WANDB_API_KEY:
    raise ValueError("WANDB API key not found in either .env file or .txt file")


# Set the environment variable and log in to wandb
os.environ["WANDB_API_KEY"] = WANDB_API_KEY
wandb.login()


# Init and download the model from wandb
run = wandb.init()
artifact = run.use_artifact('rehab-ai/rehab-ai-main/model-vgg16_False:latest')
artifact_dir = artifact.download()
model = tf.keras.models.load_model(artifact_dir)

#model = tf.keras.models.load_model("model-best.h5")

# Create your views here.
@csrf_exempt
def model_response(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    #print(body_data)

    response_data = {}
    image_height, image_width = 224, 224
    num_channels = 3

    for key in body_data:

        urls = body_data[key]
        images = []
        for url in urls:

            # get and preprocess image
            image = tf.image.decode_jpeg(
                requests.get(url).content, channels = num_channels
            )
            #print(image.shape)
            image = tf.image.resize(image, [image_height, image_width])
            #image = tf.cast(image, tf.uint8)
            images.append(image)

        # predict classification of image
        preds = model.predict(np.array(images))
        preds = [round(preds[i][0]) for i in range(preds.shape[0])]
        pred_final = max(set(preds), key=preds.count)
        #print(preds)
        response_data[key] = pred_final

    #data = {
    #    "Message": "Hello World"
    #}
    # test data
    #{
    #"20475887": ["https://photos.zillowstatic.com/fp/306c91504435f821b222f2e5acb36d0d-cc_ft_1536.jpg", "https://photos.zillowstatic.com/fp/306c91504435f821b222f2e5acb36d0d-cc_ft_1536.jpg"]
    #}
    return JsonResponse(response_data)

