# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim



# Copy local code to the container image.
# ENV APP_HOME /app
# WORKDIR $APP_HOME
COPY executor.py ./executor.py
COPY pipeline.py ./pipeline.py
COPY main.py ./dataops-pipeline

ENV PATH=$PATH:/app/

ENTRYPOINT ['/app/dataops-pipeline']
