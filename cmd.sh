#!/bin/sh

export FLASK_SECRET_KEY=$(openssl rand -base64 32)
export CSRF_SECRET=$(openssl rand -base64 32)

exec gunicorn --bind :$PORT --conf gunicorn_conf.py app:app
