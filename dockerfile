FROM python:3.10.2

RUN mkdir /opt/app
WORKDIR /opt/app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .