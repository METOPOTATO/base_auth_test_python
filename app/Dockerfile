FROM python:3.9.6

WORKDIR /base

# RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

COPY . .
