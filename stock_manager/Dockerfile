# syntax=docker/dockerfile:1
FROM python:3.11.5-alpine
RUN apk update && apk add python3-dev gcc libc-dev
RUN pip3 install --upgrade pip setuptools
RUN pip install gunicorn

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /stock_manager

COPY requirements.txt /stock_manager
RUN pip install -r requirements.txt
COPY . /stock_manager/