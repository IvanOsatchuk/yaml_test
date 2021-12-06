FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /opt/pipeline/

COPY cdf-pipeline/requirements.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
COPY cdf-pipeline/templates.py ./templates.py
COPY cdf-pipeline/executor.py ./executor.py
COPY cdf-pipeline/pipeline.py ./pipeline.py
COPY cdf-pipeline/main.py ./cdf-pipeline
RUN chmod 755 cdf-pipeline

ENV PATH=$PATH:/opt/pipeline/

ENTRYPOINT ["/opt/pipeline/cdf-pipeline"]
