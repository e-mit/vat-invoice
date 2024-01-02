docker build --target test -t test:latest .

# The -td forces the container to keep running without any CMD, and as a daemon
PORT=8000 && docker run -td -p 8080:${PORT} --name test -e FLASK_LOG_LEVEL=DEBUG -e PORT=${PORT} -e COVERAGE_FILE=/home/nonroot/.cov --rm test:latest

docker exec test python -m pytest -p no:cacheprovider
docker exec test python -m bandit -r . --exclude=/tests/
docker exec test python -m pytest --cov=. tests -p no:cacheprovider
docker exec test python -m flake8 --exclude=tests/*
docker exec test python -m mypy . --exclude '/tests/'
docker exec test sh -c 'python -m pycodestyle *.py --exclude=tests/*'
docker exec test python -m pydocstyle $(find . -path . -prune -o -name '*.py' -print) --ignore=D107,D203,D213
docker exec test python -m pylint *.py
docker exec test python -m pyright *.py

docker stop -t 0 test
