FROM alpine

WORKDIR /app

COPY . ./app

ENV PATH=$PATH:/app

CMD ["python", "main.py"]

