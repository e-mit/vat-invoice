#!/bin/sh

docker build --target test -t test:latest .

# The -td forces the container to keep running without any CMD, and as a daemon
PORT=8000 && docker run -td -p 8080:${PORT} --name test -e FLASK_LOG_LEVEL=DEBUG -e PORT=${PORT} -e COVERAGE_FILE=/home/nonroot/.cov --rm test:latest

docker exec test python -m pytest -p no:cacheprovider
docker exec test python -m bandit -r . --exclude=/tests/,/venv/
docker exec test python -m pytest --cov=. tests -p no:cacheprovider
docker exec test python -m flake8 --exclude=tests/*,venv/*
docker exec test python -m mypy . --exclude 'tests/' --exclude 'venv/'
docker exec test sh -c 'python -m pycodestyle *.py --exclude=tests/*,venv/*'
docker exec test sh -c 'python -m pydocstyle $(ls *.py) --ignore=D107,D203,D213'
docker exec test sh -c 'python -m pylint *.py'
docker exec test sh -c 'python -m pyright *.py'

docker stop -t 0 test
