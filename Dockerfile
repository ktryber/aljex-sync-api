ARG REQUIREMENTS_HASH
ARG PROJECT_NAME
ARG PROJECT_ID=dray-app
FROM us.gcr.io/${PROJECT_ID}/${PROJECT_NAME}-base:${REQUIREMENTS_HASH}
MAINTAINER Anthony Sutardja <anthony@draytechnologies.com>

# Application folder
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/secrets/gcloud-svc-key.json

# Install python requirements
COPY . /usr/src/app
WORKDIR /usr/src/app/api
