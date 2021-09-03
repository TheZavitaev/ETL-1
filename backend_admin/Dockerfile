FROM python:3.9-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN set -xe; \
    apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq netcat

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY requirements/base.txt /usr/src/app
COPY requirements/prod.txt /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r prod.txt
RUN pip install -U drf-yasg

# copy project
COPY . /usr/src/app/

# run entrypoint.prod.sh
ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]