FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /app/

COPY ./requirements.py ./requirements.py
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
COPY ./executor.py ./executor.py
COPY ./pipeline.py ./pipeline.py
COPY ./main.py ./main
RUN chmod 755 main

ENV PATH=$PATH:/app/

ENTRYPOINT ["/app/main"]
