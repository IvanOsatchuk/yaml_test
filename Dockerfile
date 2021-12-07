FROM gcr.io/google.com/cloudsdktool/cloud-sdk

WORKDIR /app/

COPY . ./app
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r ./app/requirements.txt

RUN chmod 755 ./app/main.py

ENV PATH=$PATH:/app/

ENTRYPOINT ["./app/main.py"]
