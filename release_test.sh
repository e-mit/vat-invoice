docker build --target release -t release:latest .

PORT=8000 && docker run -d -p 8080:${PORT} --name release -e PORT=${PORT} --rm release:latest

#docker stop -t 0 release
