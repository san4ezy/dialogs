FROM python:3.9.0-slim-buster
MAINTAINER Alexander Yudkin <san4ezy@gmail.com>

# Base dir
ENV PROJECT_DIR "/app"

# packages
RUN apt-get update
RUN apt-get install -y libxslt-dev libxml2-dev libpam-dev libedit-dev postgresql libpq-dev libpq-dev libgdal-dev gdal-bin python-gdal python3-gdal netcat \
    && rm -rf /var/lib/apt/lists/*

## replace default command interpreter to `bash` to be able to use `source`
#RUN ln -snf /bin/bash /bin/sh

RUN mkdir $PROJECT_DIR
WORKDIR $PROJECT_DIR

COPY requirements.txt /app/
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . $PROJECT_DIR

#COPY ./docker-entrypoint.sh /docker-entrypoint.sh
#RUN chmod +x /docker-entrypoint.sh
#ENTRYPOINT ["/docker-entrypoint.sh"]