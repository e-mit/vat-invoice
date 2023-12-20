docker build --target test -t test:latest .

# The -td forces the container to keep running without any CMD
PORT=8000 && docker run -td -p 8080:${PORT} --name test -e FLASK_LOG_LEVEL=DEBUG -e PORT=${PORT} --rm test:latest

docker exec test python -m pytest -p no:cacheprovider

docker stop -t 0 test
