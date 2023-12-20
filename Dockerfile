# syntax=docker/dockerfile:1

FROM python:3.11-alpine as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache openssl

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM base as intermediate
RUN rm -Rf tests

FROM intermediate as release
RUN adduser -D nonroot
USER nonroot
CMD ./cmd.sh

FROM base as test
RUN adduser -D nonroot
USER nonroot
RUN pip install --no-cache-dir -r requirements_test.txt
# Now wait for test commands passed with "exec"
