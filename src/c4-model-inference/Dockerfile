FROM python:3.9-slim-buster

ENV PYENV_SHELL=/bin/bash

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    pip install django && \
    pip install djangorestframework && \
    pip install requests && \
    pip install numpy && \
    pip install tensorflow && \
    pip install wandb && \
    pip install python-dotenv && \
    pip install django-cors-headers

WORKDIR /app

ADD Pipfile Pipfile.lock /app/

#RUN pipenv sync

#RUN pipenv install --system --deploy

ADD . /app

WORKDIR /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]