SET IMAGE_NAME="ansible"
SET GCP_PROJECT="ac215-project-evan2023"
SET GCP_ZONE="us-central1-a"
SET GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json
docker build -t %IMAGE_NAME% -f Dockerfile .
cd ..
docker run --rm --name %IMAGE_NAME% -ti ^
           -v /var/run/docker.sock:/var/run/docker.sock ^
           --mount type=bind,source="%cd%\secrets",target=/secrets ^
           --mount type=bind,source="C:\Users\Evan\.ssh",target=/home/app/.ssh ^
           -e GOOGLE_APPLICATION_CREDENTIALS="%GOOGLE_APPLICATION_CREDENTIALS%" ^
           -e GCP_PROJECT="%GCP_PROJECT%" ^
           -e GCP_ZONE="%GCP_ZONE%" %IMAGE_NAME%
