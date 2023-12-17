# syntax=docker/dockerfile:1

FROM python:3.11-alpine as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache openssl
#RUN apk add --no-cache wkhtmltopdf

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-privileged user that the app will run under.
RUN adduser -D nonroot
USER nonroot

EXPOSE 5000

COPY . .
