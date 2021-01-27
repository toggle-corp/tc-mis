# pull official base image
FROM python:3.9.1-slim-buster

RUN apt-get update \
    && apt-get -y install \
    && apt-get -y install postgresql postgresql-contrib build-essential \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r /app/requirements.txt