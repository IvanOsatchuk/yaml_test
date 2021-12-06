FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /opt/pipeline/

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
COPY ./executor.py .
COPY ./pipeline.py .
COPY ./main.py ./migration-pipeline
RUN chmod 755 migration-pipeline

ENV PATH=$PATH:/opt/pipeline/

ENTRYPOINT ["/opt/pipeline/migration-pipeline"]
