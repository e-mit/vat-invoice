#!/bin/sh

exec gunicorn --bind :$PORT --conf gunicorn_conf.py app:app
