FROM python:3.9-slim

WORKDIR /etl

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN set -xe; \
    apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq netcat

COPY ./entrypoint.sh /etl/entrypoint.sh

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /etl/

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U drf-yasg

ENTRYPOINT ["bash", "/etl/entrypoint.sh"]