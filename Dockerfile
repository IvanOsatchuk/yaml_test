FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /opt/pipeline/

COPY script_build/requirements.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
COPY script_build/executor.py ./executor.py
COPY script_build/pipeline.py ./pipeline.py
COPY script_build/main.py ./teste
RUN chmod 755 teste

ENV PATH=$PATH:/opt/pipeline/

ENTRYPOINT ["/opt/pipeline/teste"]
