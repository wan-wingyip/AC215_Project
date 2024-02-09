# Container 4 - Final model + inferencing

Purpose of this container is to host our final model and create an endpoint that will allow users to pass data into the final model for prediction.

The code in this container contains the final model (currently a LinearRegression model trained on the Boston housing dataset, but this will be changed later for our needs) and a Flask app that loads the final model and contains an endpoint which will accept a JSON object - this object should contain the data needed to pass into the final model to make predictions.

## How to run the container
First build the Docker image by running the following command: 
`docker build -t rehab -f Dockerfile .`

Next start up a Docker container by running the following command:
`docker run -ti -p 8080:8080 rehab `
This will allow the Docker container to be exposed to the outside through the port 8080.

Download all necessary packages using the following command:
`pipenv install`

Then run the following command to start the Flask app:
`python cli.py`

To test whether the port has been exposed and the model can make predictions, the following is an example of an API call made in Postman:
1. Make sure the API call is set to POST, and input the following URL:
`http://localhost:8080/predict`
2. Set the body of the API call to a JSON object; an example of an object that will work with the model is:
`{
    "LSTAT": [4.98, 5],
    "RM": [6.575, 9.8]
}`
3. Finally, send the API call to receive a response; an example of a response is:
`{
    "predictions": [
        28.94101368060253,
        45.358857763402995
    ]
}`
