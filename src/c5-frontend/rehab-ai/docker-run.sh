# script to RUN a docker container from the image

echo "Running the docker image for the frontend server..."
docker run -it --expose 3000 -p 80:3000 vertex-ai-pipeline:c5b-front-end:latest