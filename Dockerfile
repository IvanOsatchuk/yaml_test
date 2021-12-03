FROM alpine

WORKDIR /app

COPY . ./app

ENV PATH=$PATH:/app

