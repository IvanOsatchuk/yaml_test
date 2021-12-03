FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /opt/pipeline/


RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r
COPY main.py ./main
RUN chmod 755 main

ENV PATH=$PATH:/opt/pipeline/

ENTRYPOINT ["/opt/pipeline/main"]
