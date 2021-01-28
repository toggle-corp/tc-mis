# pull official base image
FROM python:3.9.1-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install \
    && apt-get -y install postgresql postgresql-contrib build-essential \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./