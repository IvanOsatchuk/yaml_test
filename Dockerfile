FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /app/

COPY . .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

RUN chmod 755 /app/main.py

ENV PATH=$PATH:/opt/pipeline/

ENTRYPOINT ["/app/main.py"]
