FROM python:3.5.3
MAINTAINER Anthony Sutardja <anthony@draytechnologies.com>

RUN apt-get update && apt-get install -y build-essential python3-dev

# Application folder
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install python requirements
COPY . /tmp/py/requirements
RUN pip install -r /tmp/py/requirements/prod.txt
