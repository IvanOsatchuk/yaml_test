# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
# ENV APP_HOME /app
# WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN apt update && apt -y install curl
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin/
RUN gcloud components install beta
