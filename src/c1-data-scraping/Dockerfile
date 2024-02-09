# Use an official Python runtime as a parent image
FROM python:3.9-slim

ARG DEBIAN_PACKAGES="build-essential git curl"

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell pipenv where the shell is. This allows us to use "pipenv shell" as a
# container entry point.
ENV PYENV_SHELL=/bin/bash

# Tell Python to disable buffering so we don't lose any logs.
ENV PYTHONUNBUFFERED=1

# Ensure we have an up to date baseline, install dependencies
RUN set -ex; \
    for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Lock environment
RUN pipenv lock

# Sync environment
RUN pipenv sync

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="../secrets/gcp-rehab-ai-secret.json"

# Run your script when the container launches
# ENTRYPOINT ["/bin/bash"]

# Automatically run a docker-entrypoint script when the container launches
ENTRYPOINT ["/bin/bash", ".docker-entrypoint.sh"]
