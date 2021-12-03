FROM ubuntu:16.04

MAINTAINER xyz "xyz@gmail.com"

RUN <<EOR
    apt-get update 
    apt-get install -y software-properties-common vim 
    add-apt-repository ppa:jonathonf/python-3.6 
    apt-get update -y 
    apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv 
    pip3 install --upgrade pip
    EOR


WORKDIR /app

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
