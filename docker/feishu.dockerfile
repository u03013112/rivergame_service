FROM python:3.11-slim-bullseye

COPY feishu/requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /src

WORKDIR /src
