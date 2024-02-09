# Use the official Debian-hosted Python image
FROM python:3.8-slim-buster

# Tell pipenv where the shell is. 
# This allows us to use "pipenv shell" as a container entry point.
ENV PYENV_SHELL=/bin/bash

ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/ac215-project-evan2023-2cf6235d1e3e.json

# Ensure we have an up to date baseline, install dependencies 
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    pipenv install pillow && \
    pipenv install Pillow && \
    pipenv install dvc && \
    pipenv install dvc-gs && \
    pipenv install opencv-python && \
    mkdir -p /app pipenv

WORKDIR /app

# Add Pipfile, Pipfile.lock
ADD Pipfile Pipfile.lock /app/

RUN pipenv sync

# Source code
ADD . /app

# Entry point
ENTRYPOINT ["/bin/bash"]

# Get into the pipenv shell
CMD ["-c", "pipenv shell"]
