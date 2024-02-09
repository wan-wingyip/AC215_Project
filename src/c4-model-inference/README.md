# Container 4 - Final model + inferencing

Purpose of this container is to host our final model and create an endpoint that will allow users to pass data into the final model for prediction.

The code in this container contains the final model hosted on a Django REST API endpoint. The final model is pulled from wandb and passed to tensorflow. The model is hosted on the server at port 8000 with the /model endpoint. It accepts a JSON object in the format { "<zillow-property-id>": ["<zillow-property-urls>"] }. 

## How to run the container
You can download the container from DockerHub at: 
`docker pull fk798/c4-model-inference:ms5`

Next start up a Docker container by running the following command:
`docker run -v /secrets:/secrets -p 8000:8000 fk798/c4-model-inference:ms5`
This will allow the Docker container to be exposed to the outside through the port 8000. The /secrets folder is where the wandb API key is located.

To test whether the port has been exposed and the model can make predictions, the following is an example of an API call made in Postman:
1. Make sure the API call is set to POST, and input the following URL:
`http://localhost:8080/model`
2. Set the body of the API call to a JSON object; an example of an object that will work with the model is:
`{
    "20475887": ["https://photos.zillowstatic.com/fp/306c91504435f821b222f2e5acb36d0d-cc_ft_1536.jpg", "https://photos.zillowstatic.com/fp/7687c97e0f2b53535e62618068a123be-cc_ft_1536.jpg"]
}`
3. Finally, send the API call to receive a response; an example of a response is:
`{
    "20475887": 1

}`
Note: this will work if you have a model similar to ours, or if you have the API key we use to host our models.

To test our model hosted on a GCP VM, feel free to hit this url (if it is currently up and running :^)): http://34.170.66.203:8000/model

Here is a screenshot of a Postman call to the VM: <img width="1440" alt="Screenshot 2023-11-22 at 8 43 56 PM" src="https://github.com/tonyhua18/AC215_rehab_image_detection_ai/assets/35966455/ec535e5f-b516-430a-9416-7ec847fe4041">

Here is a screenshot of the terminal from a GCP VM hosting the model: <img width="1440" alt="Screenshot 2023-11-22 at 7 22 32 PM" src="https://github.com/tonyhua18/AC215_rehab_image_detection_ai/assets/35966455/a799c602-1b04-4024-a4e1-12d127258a3c">

Here are screenshots of the terminal while predicting classifications of images: 
<img width="1440" alt="Screenshot 2023-11-22 at 7 22 39 PM" src="https://github.com/tonyhua18/AC215_rehab_image_detection_ai/assets/35966455/e14b3e09-6028-46ae-b0ab-ecbbf658b03c">

<img width="1440" alt="Screenshot 2023-11-22 at 7 31 28 PM" src="https://github.com/tonyhua18/AC215_rehab_image_detection_ai/assets/35966455/1f3cab67-0705-44cd-8708-6438dcb76a21">
