FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /opt/pipeline/

COPY yaml_test/requirements.py .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
COPY yaml_test//executor.py ./executor.py
COPY yaml_test//pipeline.py ./pipeline.py
COPY yaml_test//main.py ./main
RUN chmod 755 main

ENV PATH=$PATH:/opt/pipeline/

ENTRYPOINT ["/opt/pipeline/main"]
