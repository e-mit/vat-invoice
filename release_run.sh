#!/bin/sh

docker build --target release -t release:latest .

PORT=8000
FLASK_SECRET_KEY=$(openssl rand -base64 32)
CSRF_SECRET=$(openssl rand -base64 32)

docker run -p 8080:${PORT} --name release \
    -e PORT=${PORT} \
    -e FLASK_SECRET_KEY=${FLASK_SECRET_KEY} \
    -e CSRF_SECRET=${CSRF_SECRET} \
    --rm release:latest

# docker stop -t 0 release
